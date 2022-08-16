import numpy as np
import pandas as pd
import csv
import random


def create_word_list(file_string):
    with open(file_string) as f:
        lines = f.readlines()

    word_list = []
    for i in lines:
        word_list.append(i)

    word_list_stg = []
    for i in word_list:
        word_list_stg.append(i[:-1].lower())

    return word_list_stg

def game_setup(word, word_list):
    word = word.lower()
    word_length = len(word)

    valid_guesses = []
    for i in word_list:
        if len(i) == word_length:
            valid_guesses.append(i)

    if word not in valid_guesses:
        return "fail"

    else:
        return valid_guesses

def play_game_personal(game_word, file_string = 'words.txt'):
    word_list = create_word_list(file_string)
    valid_guesses = game_setup(game_word.lower(), word_list)
    guess_count = 0
    guessed_correct = False

    valid_guess_list, current_word_state = [], list('_'*len(game_word))
    letters_not_in_word, letters_in_position, letters_out_of_position = [],[],[]

    while guessed_correct is False:
        guess_count += 1
        guess = input("What is the word? It has " + str(len(game_word)) + " characters.    ").lower()

        if guess == game_word:
            print("CORRECT, YOU WIN! It took " + str(guess_count) + " guesses.")
            return True

        elif len(game_word) != len(guess):
            print("wrong number of letters")

        else:
            valid_guess_list.append(guess)
            for letter_position in range(len(guess)):
                #correct position, letter not position, not in word
                if guess[letter_position] not in game_word:
                    letters_not_in_word.append(guess[letter_position])
                    print(guess[letter_position] + " not in word")
                
                elif guess[letter_position] == game_word[letter_position]:
                    letters_in_position.append(guess[letter_position])
                    print(guess[letter_position] + " in word in position " + str(letter_position) )
                    current_word_state[letter_position] = guess[letter_position]

                else:
                    letters_out_of_position.append(guess[letter_position])
                    print(guess[letter_position] + " in word not in position " + str(letter_position) )
            
            print(current_word_state)
            print(valid_guess_list)
            print("letters in position: ")
            print(letters_in_position)
            print("letters not in position: " )
            print(letters_out_of_position)
            print("letters not in word: ")
            print(letters_not_in_word)


def bot_play(game_word, guess_type, file_string = 'words.txt'):
    word_list = create_word_list(file_string)
    valid_guesses = game_setup(game_word.lower(), word_list)
    guess_count = 0
    guessed_correct = False

    valid_guess_list, current_word_state = [], list('_'*len(game_word))
    letters_not_in_word, letters_in_position, letters_out_of_position = [],[],[]

    while guessed_correct is False:
        print(len(valid_guesses))

        guess_count += 1
        guess = choose_guess(valid_guesses, valid_guess_list, current_word_state, letters_not_in_word, letters_in_position, letters_out_of_position, guess_type)
        print(guess)
        if guess == game_word:
            print("CORRECT, YOU WIN! It took " + str(guess_count) + " guesses.")
            return True

        else:
            valid_guess_list.append(guess)
            for letter_position in range(len(guess)):
                if guess[letter_position] not in game_word:
                    letters_not_in_word.append(guess[letter_position])
                    print(guess[letter_position] + " not in word")

                elif guess[letter_position] == game_word[letter_position]:
                    letters_in_position.append(guess[letter_position])
                    print(guess[letter_position] + " in word in position " + str(letter_position) )
                    current_word_state[letter_position] = guess[letter_position]

                else:
                    letters_out_of_position.append(guess[letter_position])
                    print(guess[letter_position] + " in word not in position " + str(letter_position) )

            letters_not_in_word, letters_in_position, letters_out_of_position = list(set(letters_not_in_word)), list(set(letters_in_position)), list(set(letters_out_of_position))
            
            print(letters_not_in_word, letters_in_position, letters_out_of_position)
            new_valid_guesses = []
            for possible_word in valid_guesses:
                validity = True
                for letter_position in range(len(guess)):
                    if current_word_state[letter_position] == '_':
                        pass
                    else:
                        if current_word_state[letter_position] != possible_word[letter_position]:
                            validity = False

                for letter in letters_not_in_word:
                    if letter in possible_word:
                        validity = False
                for letter in letters_out_of_position:
                    if letter not in possible_word:
                        validity = False

                if possible_word in valid_guess_list:
                    validity = False

                if validity == True:
                    new_valid_guesses.append(possible_word)

            valid_guesses = new_valid_guesses

def choose_guess(valid_guesses, valid_guess_list, current_word_state, letters_not_in_word, letters_in_position, letters_out_of_position, guess_type = 'letter_scoring'):
    if guess_type == 'random':
        return random.choice(valid_guesses)

    if guess_type == 'letter_scoring':
        best_guess, best_score = None, 0
        for guess in valid_guesses:
            score = 0
            score_dictionary = {'e':11, 'a':8.5, 'r':7.5, 'i':7.5, 'o':7.2, 't':6.95, 'n':6.65, 's':5.7, 'l':5.4, 'c':4.5, 'u':3.6, 'd':3.38, 'p':3.16, 'm':3, 'h':3, 'g':2.4,
                                'b':2, 'f':1.8, 'y':1.7, 'w':1.2, 'k':1.1, 'v':1, 'x':.29, 'z':.27, 'j':.2, 'q':.2}

            for letter in guess:
                score += score_dictionary[letter]

            if score > best_score:
                best_guess, best_score = guess, score

        return best_guess

bot_play('proof','letter_scoring')