#!/usr/bin/env python3
"""
Write your code in this file. Fill out the defined functions with your solutions.
You are free to write additional functions and modules as you see fit.
"""
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

def calculate_score(points):
    """
    Assignment 3
    """
    tot = {}
    for letter in points:
        if letter.islower():
            tot[letter] = tot.get(letter, 0) + 1
        else:
            tot[letter.lower()] = tot.get(letter.lower(), 0) - 1
                
    return ", ".join([k + ":" + str(v) for k, v in sorted(tot.items(), key=itemgetter(1), reverse=True)])

def find_missing(numbers):
    """
    Assignment 4
    """
    numbers.sort()
    missing = []
    r = range(numbers[0], numbers[-1]+1)
    for i in r:
        if not i in numbers:
            missing.append(i)
    return missing

def add_range():
    """
    Assignment 5
    """
    while True:
        number = input("Enter a number: ")
        summa = 0
        if number == "q":
            break
        try:
            n = int(number)
        except ValueError:
            print("Input an integer")
            continue
        if n < 0:
            start = n
            stop = 1
        else:
            start = 1
            stop = n + 1
        for i in range(start, stop):
            if not i % 3 and not i % 5:
                continue
            if not i % 3 or not i % 5:
                summa += i
        print(summa)

if __name__ == '__main__':
    text_repetition()
    convert_to_hex(())
    calculate_score("")
    find_missing([])
    add_range()
