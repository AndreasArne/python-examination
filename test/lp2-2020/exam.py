#!/usr/bin/env python3
"""
Write your code in this file. Fill out the defined functions with your solutions.
You are free to write additional functions and modules as you see fit.
"""
import analyze_functions
from operator import itemgetter

def text_repetition():
    """
    Assignment 1
    """
    with open("repetition.txt", "r") as fh:
        ll = []
        for line in fh:
            try:
                val = int(line)
                print(", ".join([" ".join(ll)] * val) + ".")
                ll = []
            except ValueError:
                ll.append(line.strip())



def zero_pad(val):
    """
    Pad string with 0
    """
    return "0" + val if len(val) == 1 else val

def convert_to_hex(rbg_values):
    """
    Assignment 2
    """
    return "#" + zero_pad(hex(rbg_values[0])[2:]) + zero_pad(hex(rbg_values[1])[2:]) + zero_pad(hex(rbg_values[2])[2:])



def find_words(letters, words):
    """
    Assignment 3
    """
    max_word = ""
    for word in words:
        all_in_word = True
        tmp_letters = letters

        for letter in word:
            if letter in tmp_letters:
                tmp_letters = tmp_letters.replace(letter, "", 1)

            else:
                all_in_word = False
                break

        if all_in_word and len(word) > len(max_word):
            max_word = word

    return max_word



def missing_letters(letters):
    """
    Assignment 4
    """
    abc = "abcdefghijklmnopqrstuvwxyz"
    missing = []
    start_index = abc.index(letters[0])
    end_index = abc.index(letters[-1])
    letters_ind = 0
    for ind in range(start_index, end_index):
        if abc[ind] == letters[letters_ind]:
            letters_ind += 1
        else:
            missing.append(abc[ind])
    return missing


def leap_days(start, stop):
    """
    Assignment 5
    """
    if start > stop:
        return -1

    nr_leap_days = 0
    while start < stop:
        if start % 4 == 0:
            if start % 100 == 0 and start % 900 not in (200, 600):
                start += 1
                continue
            nr_leap_days += 1
        start += 1
    return nr_leap_days



if __name__ == '__main__':
    # analyze_text()
    # reversed_sum()
    # frequency_sort()
    # find_word()
    # repeating_letter_distance()
    pass