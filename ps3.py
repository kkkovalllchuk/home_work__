# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Daria Kovalchuk
# Collaborators : <your collaborators>
# Time spent    : <total time>


import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------


#
# Problem #1: Scoring a word
#
def get_word_score(word, n):

    def f(x, y):
        if x > y:
            return x
        return y

    one = 0
    for i in word.lower():
        one += SCRABBLE_LETTER_VALUES.get(i, 0)
        
    two = f((7 * len(word)) - (3 * (n - len(word))), 1)
    
    return one * two

def display_hand(hand):
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line


def deal_hand(n):
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    
    hand['*'] = 1
    num_vowels -= 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand


def update_hand(hand, word):

    copy = hand.copy()
    
    for i in word.lower():
        if copy.get(i, 0) > 0:
            copy[i] -= 1
    
    return copy


def is_valid_word(word, hand, word_list):
   
    
    def replace(word):
        list_word = []
        for vowel in VOWELS:
            index_of_wildcard = word.find('*')
            
            new_word = word[0:index_of_wildcard] + vowel            
            if index_of_wildcard < len(word) - 1:
                new_word += word[index_of_wildcard + 1:]
                
            list_word.append(new_word.lower())
            
        return list_word
            
    
    if '*' in word:
        replace_wildcard = replace(word)
        none = True
        
        for w in replace_wildcard:
            if w.lower() in word_list:
                none = False
                
        if none:
            return False
        
    elif word.lower() not in word_list:
        return False
        
    
    hand_copy = hand.copy()
    for char in word.lower():
        if char not in hand_copy.keys():
            return False
        else:
            hand_copy[char] -= 1
            if hand_copy[char] < 0:
                return False
    
    return True


def calculate_handlen(hand):
    
    number_of_letters = 0
    for value in hand.values():
        number_of_letters += value
        
    return number_of_letters


def play_hand(hand, word_list):

    score = 0

    while calculate_handlen(hand) > 0:
    
       
        print('Current Hand: ', end='')
        display_hand(hand)
        
       
        word = input('Enter word, or \"-\" to indicate that you are finished: ')
        
        
        if word == '-':
            break

        else:
            if is_valid_word(word, hand, word_list):

                
                points_earned = get_word_score(word, calculate_handlen(hand))
                score += points_earned
                print('\"{}\" earned {} points. Total: {} points'.format(word, points_earned, score))

            else:
                print('That is not a valid word. Please choose another word.')
            hand = update_hand(hand, word)
            

   
    if calculate_handlen(hand) <= 0:
        print('Ran out of letters.')
    print('Total score for this hand: {}'.format(score))

   
    return score





def substitute_hand(hand, letter):
    
    copy = hand.copy()
    
    if not letter.isalpha() or letter not in copy.keys():
        return copy
    
    num_of_items_of_current_letter =copy[letter]
    del(copy[letter])
    
    if letter in VOWELS:
        list_of_letters_to_get_new_letter_from = VOWELS
    else:
        list_of_letters_to_get_new_letter_from = CONSONANTS
        
    while True:
        new_letter = random.choice(list_of_letters_to_get_new_letter_from)
        if new_letter not in hand.keys():
            copy[new_letter] = num_of_items_of_current_letter
            break
        
    return copy
                
       
    
def play_game(word_list):
    
    overall_score = 0
    answer_to_replay_hand_question = 'no'
    total_num_of_hands = int(input('Enter total number of hands: '))
    for num_of_hands in range(total_num_of_hands):
        if num_of_hands > 0:            
            answer_to_replay_hand_question = input('Would you like to replay the hand? ')
        
        if answer_to_replay_hand_question == 'no' or 'No':
            hand = deal_hand(HAND_SIZE)
        
        print('Current Hand: ', end='')
        display_hand(hand)
        
        answer_to_substitute_question = input('Would you like to substitute a letter?Yes or no. ')
        if answer_to_substitute_question == 'yes' or 'Yes':
            letter_to_be_replaced = input('Which letter would you like to replace? ')
            hand = substitute_hand(hand, letter_to_be_replaced)
        
        overall_score += play_hand(hand, word_list)
        print('_'*20)
        
    
    print('Total score over all hands: {}'.format(overall_score))



if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)