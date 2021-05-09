from dataclasses import dataclass 
import operator

@dataclass
class Player:
    name  : str 
    points: int
    
# Set this absolute path to your answers.bin file location after downloading from repo
answers_file_path = "C:/path/answers.bin"

# Remove all whitespaces from a string
def remove_whitespaces(s: str) -> str:
    return "".join(s.split())

# Get a string input for the user. Don't accept empty inputs
def get_input(msg: str, err_msg: str) -> str:
    while True:
        ans = input(msg)

        # if input is empty ( or only contains whitespaces ). Print the error message and ask again
        if not remove_whitespaces(ans):
            print(err_msg)
            continue 

        return ans 

# print out the top 10 players from a player list
def print_top_10(players: list):
    counter = 0
    
    # sort player list according to their points
    players.sort(key=operator.attrgetter('points'), reverse=True)

    # print out the top 10 players
    for player in players:
        counter += 1
        if counter > 10:
            break 

        print(f"{counter}. {player.name} : {player.points} points")

# award a player for winning the game. If player doesn't exist then add to the list
def award_player(player_name: str, player_list: list, points: int):
    for player in player_list:
        if player_name == player.name:
            player.points += points
            return None

    player_list.append(Player(player_name, points))

# return the match % of a word with the guesses 
def get_match_percent(word: str) -> int:
    total_letter = 0
    total_matches = 0
    fil = open(answers_file_path, "rb")
    for line in fil.readlines():
        answer = line.decode().rstrip()

        for letter in answer:
            total_letter += 1 
            if letter in word:
                total_matches += 1 

    fil.close()
    return total_matches / total_letter * 100
    
    
# Check if a guess is correct 
def check_guess(guess: str) -> bool:
    fil = open(answers_file_path, "rb")
    for line in fil.readlines():
        answer = line.decode().rstrip()

        if answer == guess.lower():
            return True 

    fil.close()
    return False

# get a guess from the user
def get_guess(num_guesses: int, any_matched: bool) -> str:
    if num_guesses == 5 and any_matched:
        return get_input("Enter a word guess (Final guess): ", "Please enter a non-empty guess")

    else:
        while True:
            ans = get_input(f"Enter a letter guess ({5 - num_guesses} guesses left): ", "Please enter a non-empty guess")

            if len(ans) == 1 and ans.isalpha(): return ans 
            print("Please enter a letter. ", end="")

# check if user wants to play the game again
def wants_to_play_again() -> bool:
    return input("Welcome to Hangman! Enter 'p' to play, anything else to quit: ").lower() == 'p'

# update the player list after a game ends
def update_player_list(players: list, points: int):
    user_name = get_input("Enter your username: ", "Please enter a non-empty username").lower()
    award_player(user_name, players, points)


def main():
    players=[]
    choice = get_input("Welcome to Hangman! Enter 'p' to play, anything else to quit: ", "Please enter a valid choice!")

    # exit if choice wasn't 'p'( play )
    if choice.lower() != 'p': 
        exit()

    num_guesses = 0
    any_matched = False
    while True:
        # check if the player ran out of guesses
        if (num_guesses > 5) or (num_guesses > 4 and (not any_matched)) :
            print("You ran out of guesses!")
            update_player_list(players, 0)
            print_top_10(players)
            if not wants_to_play_again(): break

            # reset counters
            num_guesses = 0
            any_matched = False

        guess = get_guess(num_guesses, any_matched)
        match_amount = int(get_match_percent(guess))

        print(f"Guess {guess} has a {match_amount}% match")             

        # update the any matched variable to see if either of the letter guesses were correct
        if match_amount > 0: any_matched = True

        # check if the player won the game on the last guess
        if num_guesses == 5 and check_guess(guess):
            print("Congratulations! You guessed the word correctly!")
            update_player_list(players, 10)
            print_top_10(players)
            if not wants_to_play_again(): break
            
            # reset counters
            num_guesses = 0
            any_matched = False
            continue

        # increment number of guesses if player didn't win or run out of guesses
        num_guesses += 1
        
# run main
if __name__ == "__main__":
    main()