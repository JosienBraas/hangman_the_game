# Hangman, The Game!
# Created by Josien Braas to practice Python

import random
import string
import sys
import time

# If a dictionary file is specified, use it -
# otherwise, use a default dictionary
if len(sys.argv) > 1:
    dictionary_file = sys.argv[1]
else:
    dictionary_file = 'dictionary.txt'

game_state = [
    """






     _____________
""",
    """

    |
    |
    |
    |
    |
    |_____________
""",
    """
    _________
    |
    |
    |
    |
    |
    |_____________
""",
    """
    _________
    |         |
    |
    |
    |
    |
    |_____________
""",
    """
    _________
    |         |
    |         0
    |
    |
    |
    |_____________
""",
    """
    _________
    |         |
    |         0
    |         |
    |
    |
    |_____________
""",
    """
    _________
    |         |
    |         0
    |        /|\\
    |
    |
    |_____________
""",
    """
    _________
    |         |
    |         0
    |        /|\\
    |        /
    |
    |_____________
""",
    """
    _________
    |         |
    |         0
    |        /|\\
    |        / \\
    |
    |_____________
"""
]


def start_game():
    """
    Initialize the game and execute the game turns. A
    new game starts with score 0 for both the player
    and the computer. Subsequent game rounds should be
    called with the updated scores.
    """

    # Initialize the game
    player_score = 0
    computer_score = 0
    print("\nWelcome to Hangman, The Game!")
    print("\nWhat is your name?")
    player_name = input("> ")
    time.sleep(0.4)
    print("\nHi " + player_name + ", let's play!")
    time.sleep(0.6)

    # Start the game loop
    while True:
        word = pick_word()
        current_state = 0
        guess_list = []
        game_ended = False

        print("\n--------------------\nHangman Rules\n"
              + """
The rules are as follows. You have to guess the word
before the hanging is completed. For every letter you
guessed that is not part of the word, the hanging
advances one step... Have fun!""")

        # Process turns
        while not game_ended:

            while True:
                player_guess = input("\nGuess a letter: ")
                if len(check_guess(player_guess, guess_list)) == 0:
                    break
                print(check_guess(player_guess, guess_list))

            guess_list.append(player_guess.lower())

            if player_guess not in word:
                current_state = current_state + 1
                print("Uh oh! That letter is not in the word: "
                      + show_word(word, guess_list)
                      + "\n"
                      + game_state[current_state])
            else:
                print("Good guess! The word is now: "
                      + show_word(word, guess_list))

            # Win condition
            if check_win(word, guess_list) and current_state < 8:
                game_ended = True
                player_score += 1
                print("\n>> YOU WIN! <<\n")
                print("The score is now:")
                print("Player " + str(player_score) + " - Computer "
                      + str(computer_score) + "\n")
            # Lose condition
            elif current_state == 8:
                game_ended = True
                computer_score += 1
                print("\nThe word was: "
                      + show_word(word, list(string.ascii_lowercase)))
                print("\n>> YOU LOSE! <<\n")
                print("The score is now:")
                print("Player " + str(player_score) + " - Computer "
                      + str(computer_score) + "\n")

        print("Do you want to play another game?")
        choice = input("y/n: ")

        if choice != 'y' and choice != 'Y':
            break


def pick_word(minimum_length=8):
    """() -> string

    Return a random word from the dictionary file. The minimum
    length of the word can optionally be provided as a parameter.
    """
    with open(dictionary_file, 'r') as file_object:
        words = file_object.readlines()
        # Make sure that this loop has an ending:
        max_length = len(max(words, key=len)) - 1
        if max_length < minimum_length:
            minimum_length = max_length
        while True:
            random_word = random.choice(words).replace('\n', '')
            if len(random_word) >= minimum_length:
                word = random_word
                break
    return word


def check_guess(player_guess, guesses):
    """(string, [string]) -> string

    Check if the guess provided by the user is a correct guess -
    that is, one that is just 1 letter and not guessed before.

    >>> check_guess('', [])
    'Please enter at least one letter.'
    >>> check_guess('bacon', [])
    'Please enter only one character.'
    >>> check_guess('c', ['f', 'c', 'g', 'e'])
    'Please pick a letter you did not guess before.'
    >>> check_guess('bacon', ['c', 'a', 'b', 'o', 'n'])
    'Please enter only one character.'
    """
    message = ""
    if len(player_guess) == 1:
        if player_guess not in string.ascii_letters:
            message = "Please enter only letters."
        elif player_guess.lower() in guesses:
            message = "Please pick a letter you did not guess before."
    elif len(player_guess) == 0:
        message = "Please enter at least one letter."
    else:
        message = "Please enter only one character."
    return message


def show_word(word, guesses):
    """(string, [string]) -> string

    Return the word to guess with guessed letters filled in and
    underscores for un-guessed letters.

    >>> show_word("", [])
    ''
    >>> show_word("bacon", [])
    '_ _ _ _ _'
    >>> show_word("bacon", ['f', 'c', 'g', 'e'])
    '_ _ c _ _'
    >>> show_word("bacon", ['c', 'a', 'b', 'o', 'n'])
    'b a c o n'
    """
    word_list = list(word)
    for i, element in enumerate(word_list):
        if element not in guesses:
            word_list[i] = '_'
    return " ".join(word_list)


def check_win(word, guesses):
    """(string, [string]) -> bool

    Return the guess status of a word based on the word to be guessed
    and the guesses a player has made.

    >>> check_win("", [])
    True
    >>> check_win("bacon", [])
    False
    >>> check_win("bacon", ['f', 'c', 'g', 'e'])
    False
    >>> check_win("bacon", ['c', 'a', 'b', 'o', 'n'])
    True
    """
    state = True
    for letter in word:
        if letter not in guesses:
            state = False
    return state


if __name__ == "__main__":
    start_game()
