#!/usr/local/bin/python
from enum import Enum
import random
import datetime
import csv
import sys
import time

max_attempts = 10000
max_builds = 2000

class Status(Enum):
    EMPTY = 1
    OCCUPIED = 2
    MATCH = 3

class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    UNKNOWN = 3

class Mode(Enum):
    RANDOM = 1
    SYSTEMATIC = 2
    CENTRE = 3

def create_crossword(words):
    # Sort words by length in descending order
    # ie. Place the largest words first while the grid is clear
    words.sort(key=lambda x: len(x[0]), reverse=True)

    # When placing vertically, the first letter must be clear above and the last
    # letter must be clear below
    def is_clear_vertical(grid, letter, row, col):
        # print("Testing vertical position: " + str(row) + ", " + str(col))
        # If the letter is already in that square, all good
        # This crossover over words is actually the ideal situation
        # so let's weight this outcome higher.
        if grid[row][col] == letter:
            return Status.MATCH

        if grid[row][col] != '#':
            # The square doesn't contain the letter being places and
            # isn't clear so can't go there.
            return Status.OCCUPIED
        
        if col == 20:
            # Check cell is clear to the left as we are against the
            # left hand edge of the grid
            if grid[row][col-1] != '#':
                return Status.OCCUPIED
            
            return Status.EMPTY
            
        if col == 0:
            # Check cell is clear to the right as we are against the
            # left hand edge of the grid
            if grid[row][col+1] != '#':
                return Status.OCCUPIED
            
            return Status.EMPTY
        
        # We are somewhere in the middle so check side to side
        if grid[row][col-1] != '#' or grid[row][col+1] != '#':
            return Status.OCCUPIED

        return Status.EMPTY
    
    # When placing horizontally, the first letter must be clear to the left and
    # the last letter must be clear to the right
    def is_clear_horizontal(grid, letter, row, col):
        # print("Testing horizontal position: " + str(row) + ", " + str(col))
        # If the letter is already in that square, all good if it is crossing
        # but not good if extending a word.
        if grid[row][col] == letter:
            return Status.MATCH
        
        if grid[row][col] != '#':
            # The square doesn't contain the letter being places and
            # isn't clear so can't go there.
            return Status.OCCUPIED
        
        # Check cell is clear above and below
        if row == 20:
            # Check cell is clear to the above as we are against the
            # bottom edge of the grid
            if grid[row-1][col] != '#':
                return Status.OCCUPIED
            
            return Status.MATCH
            
        if row == 0:
            # Check cell is clear to the below as we are against the
            # top edge of the grid
            if grid[row+1][col] != '#':
                return Status.OCCUPIED

            return Status.EMPTY
    
        # We are somewhere in the middle so check above and below
        if grid[row-1][col] != '#' or grid[row+1][col] != '#':
            return Status.OCCUPIED

        return Status.EMPTY
    
    # Function to check if a word can be placed horizontally at a specific position.
    # The more valid interactions with other words the better so return a score for
    # the specified word in the specified position.
    # -1 means can't go here
    #  0 means can go here but doesn't cross any other words
    # >0 indicates the number of other words it crosses when put here 
    def can_place_horizontally(grid, word, row, col):
        # Keep a record of how good this position is for this word
        score = 0

        # If the position plus the length of the word goes off the grid
        # it clearly can't be placed here.
        # print ("Final square will be col: " + str(col + len(word)))
        if col + len(word) > 21:
            return -1
    
        # Check each letter and the surrounding cells. 
        for i in range(len(word)):
            if i == 0:
                # This is the first letter so also check the left is clear
                if col - 1 > -1 and grid[row][col - 1] != '#':
                    return -1 
        
            if i == len(word) - 1:
                # This is the last letter so also check the right is clear
                if col + i + 1 < 21:
                    #print("Last letter (" + word[i] + ") check for word " + word + " has square " + grid[row][col + i + 1])
                    if grid[row][col + i + 1] != '#':
                        return -1 
                           
            result = is_clear_horizontal(grid, word[i], row, col + i)

            if result == Status.OCCUPIED:
                # The word can't go here at all
                return -1
            
            if result == Status.MATCH:
                score += 1

            # The other option is Status.EMPTY which required no action.
            # It's not a reason to abort and not a reason to increment the score.
            
        return score

    # Function to check if a word can be placed vertically at a specific position
    def can_place_vertically(grid, word, row, col):
        # Keep a record of how good this position is for this word
        score = 0

        # If the position plus the length of the word goes off the grid
        # it clearly can't be placed here.
        # print ("Final square will be row: " + str(row + len(word)))
        if row + len(word) > 21:
            return -1
        
        # Check each letter and the surrounding cells
        for i in range(len(word)):
            if i == 0:
                # This is the first letter so also check above is clear
                if row - 1 > -1 and grid[row - 1][col] != '#':
                    return -1 
        
            if i == len(word) - 1:
                # print("Last word check")
                # This is the last letter so also check below is clear
                if row + i + 1 < 21:
                    #print("Last letter (" + word[i] + ") check for word " + word + " has square " + grid[row + i + 1][col])
                    if grid[row + i + 1][col] != '#':
                        return -1 
                      
            result = is_clear_vertical(grid, word[i], row + i, col)

            if result == Status.OCCUPIED:
                # The word can't go here at all
                return -1
            
            if result == Status.MATCH:
                score += 1

        return score

    # Function to build a whole grid
    def build_grid(words):
        # Place words on the grid
        placed_words = []

        # Clear the grid for this run
        grid = [['#' for _ in range(21)] for _ in range(21)]

        # Start in centre mode while placing the first word as it is also the
        # longest word.
        mode = Mode.CENTRE

        for word_and_clue in words:
            word, clue = word_and_clue
            best_score = 0
            best_position = (0, 0, Orientation.UNKNOWN)

            # Make attempts at each word and chose the base location.
            if mode == Mode.RANDOM:
                attempts = 0
                while attempts < max_attempts:
                    # Pick a random square to start from
                    row = random.randint(0, 20)
                    col = random.randint(0, 20)

                    # Test fit the word going down and across from the chosen starting square
                    horizonal_score = can_place_horizontally(grid, word, row, col)
                    vertical_score = can_place_vertically(grid, word, row, col)

                    # Which was best out of horizontal and vertical?
                    # Was it better than the best so far?
                    if horizonal_score >= vertical_score:
                        if horizonal_score >= best_score:
                            best_score = horizonal_score
                            best_position = (row, col, Orientation.HORIZONTAL)
                    else: 
                        if vertical_score >= best_score:
                            best_score = vertical_score
                            best_position = (row, col, Orientation.VERTICAL)

                    attempts += 1

            elif mode == Mode.CENTRE:
                centre_column = int((21 - len(word)) / 2)
                best_position = (10, centre_column, Orientation.HORIZONTAL)

                # This is the first word placement so it can only have
                # succeeded, break and place it.
                mode = Mode.RANDOM

            elif mode == Mode.SYSTEMATIC:
                for row in range(21):
                    for col in range(21):
                        # Test fit the word going down and across from the chosen starting square
                        horizonal_score = can_place_horizontally(grid, word, row, col)
                        vertical_score = can_place_vertically(grid, word, row, col)

                        # Which was best out of horizontal and vertical?
                        # Was it better than the best so far?
                        if horizonal_score >= vertical_score:
                            if horizonal_score >= best_score:
                                best_score = horizonal_score
                                best_position = (row, col, Orientation.HORIZONTAL)
                        else: 
                            if vertical_score >= best_score:
                                best_score = vertical_score
                                best_position = (row, col, Orientation.VERTICAL)

            chosen_row, chosen_column, chosen_orientation = best_position

            # Was a position successfully found?       
            if chosen_orientation == Orientation.HORIZONTAL:
                for i in range(len(word)):
                    grid[chosen_row][chosen_column + i] = word[i]
                
                placed_words.append((word, (chosen_row * 21) + chosen_column + 1, clue, Orientation.HORIZONTAL))


            elif chosen_orientation == Orientation.VERTICAL:
                for i in range(len(word)):
                    grid[chosen_row + i][chosen_column] = word[i]

                placed_words.append((word, (chosen_row * 21) + chosen_column + 1, clue, Orientation.VERTICAL))
        
            else:
                # If the chosen orientation is UNKNOWN then the word can't have
                # been placed so time to switch to SYSTEMATIC mode for the rest of the words
                mode = Mode.SYSTEMATIC

        return placed_words, grid


    # Record how long the generation takes
    start_time = time.time()

    best_so_far = 0
    best_words = []
    best_grid = []

    builds = 0
    while builds < max_builds:
        placed_words, grid = build_grid(words)
        # print("This time we placed " + str(len(placed_words)))
        if (len(placed_words) > best_so_far):
            best_so_far = len(placed_words)
            print("New best grid with " + str(best_so_far) + " words.", file=sys.stderr)
            best_words = placed_words
            best_grid = grid

        builds += 1

    # Convert grid to a printable string
    crossword = '\n'.join([''.join(row) for row in best_grid])

    elapsed_time = time.time() - start_time

    return crossword, best_words, elapsed_time

# Check if a filename was provided
if len(sys.argv) < 2:
    print("Usage: python script.py filename.csv")
    sys.exit(1)  # Exit the script with an error status

filename = sys.argv[1]  # Get the filename from command line arguments

# List to hold words and clues
words_and_clues = []

# Reading the CSV file
delimiter = '\t' if filename.endswith('.tsv') else ','  # Set delimiter based on file extension

try:
    with open(filename, newline='') as file:
        reader = csv.reader(file, delimiter=delimiter)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 2:  # Ensuring there are at least two columns
                word = row[0].strip().upper()  # Clean up any extra whitespace
                clue = row[1].strip().capitalize() # Capitalise the first letter of the clue
                words_and_clues.append((word, clue))  # Append the word and clue as a tuple
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

crossword, placed_words, elapsed_time = create_crossword(words_and_clues)

# Print the metadata
print("Title: " + filename)
print("Words: " + str(len(placed_words)) + " placed out of " + str(len(words_and_clues)))
print("Gen time: " + str(int(elapsed_time)) + " seconds")
print("Date: " + str(datetime.date.today()))
print("\n")


# Print the crossword grid
print(crossword)

print("\n")

sorted_across = []
sorted_down = []

#print("This is the order they were placed.")
#for placed_word in placed_words:
#    print(placed_word)

# Sort the words into order of the square they start in
placed_words.sort(key=lambda word: word[1])

#print("This is the sorted order.")
#for placed_word in placed_words:
#    print(placed_word)

# Reduce the starting squares to a sequential order
ordered_words = []

clue_number = 0
last_square = -1

# We need to order the words sequentially, but clues that start on the
# same square need to have the same clue number
for i in range(len(placed_words)):
    word, square, clue, orientation = placed_words[i]  # Unpack the current tuple

    #print("Word is " + word + ", last square is " + str(last_square) + " and this square is " + str(square))

    if (last_square == square):
        # This clue starts in the same square as the last so don't
        # increment the clue_number
        # print("Adding word " + word + " without incrementing clue number.")
        ordered_words.append((word, clue_number, clue, orientation))
    else:
        clue_number += 1
        ordered_words.append((word, clue_number, clue, orientation))
    
    last_square = square

# print(ordered_words)

for i in range(len(ordered_words)):
    word, square, clue, orientation = ordered_words[i]  # Unpack the current tuple
    if orientation == Orientation.HORIZONTAL:
        sorted_across.append((word, square, clue))

for i in range(len(ordered_words)):
    word, square, clue, orientation = ordered_words[i]  # Unpack the current tuple
    if orientation == Orientation.VERTICAL:
        sorted_down.append((word, square, clue)) 
    
# Print the updated positions of the words
for word, number, clue in sorted_across:
    print(f"A{number}. {clue}")

print("")

for word, number, clue in sorted_down:
    print(f"D{number}. {clue}")

