#!/usr/local/bin/python
import random
import datetime

def create_crossword(words):
    # Create an empty grid
    grid = [['#' for _ in range(21)] for _ in range(21)]

    # Sort words by length in descending order
    words.sort(key=lambda x: len(x), reverse=True)

    # Helper function to check cells around a given position

    # The first letter must be clear above and the last
    # letter must be clear below
    def is_clear_vertical(letter, row, col):
        # If the letter is already in that square, all good
        if grid[row][col] == letter:
            return True

        if grid[row][col] != '#':
            # The square doesn't contain the letter being places and
            # isn't clear so can't go there.
            return False
        
        # Check cell is clear side to side
        if col == 20:
            # Only need to check above as we are on the bottom row
            if grid[row][col-1] != '#':
                return False
            
            return True
            
        if col == 0:
            # Only need to check below as we are on the top row
            if grid[row][col+1] != '#':
                return False
            
            return True
        
        # We are somewhere in the middle so check above and below
        if grid[row][col-1] != '#' or grid[row][col+1] != '#':
            return False

        return True
    
    # The first letter must be clear to the left and
    # the last letter must be clear to the right
    def is_clear_horizontal(letter, row, col):
        # If the letter is already in that square, all good
        if grid[row][col] == letter:
            return True
        
        if grid[row][col] != '#':
            # The square doesn't contain the letter being places and
            # isn't clear so can't go there.
            return False
        
        # Check cell is clear above and below
        if row == 20:
            # Only need to check above as we are on the bottom row
            if grid[row-1][col] != '#':
                return False
            
            return True
            
        if row == 0:
            # Only need to check below as we are on the top row
            if grid[row+1][col] != '#':
                return False

            return True
    
        # We are somewhere in the middle so check above and below
        if grid[row-1][col] != '#' or grid[row+1][col] != '#':
            return False

        return True
    
    # Function to check if a word can be placed horizontally at a specific position
    def can_place_horizontally(word, row, col):
        if col + len(word) > 21:
            return False
    
        # Check each letter and the surrounding cells
        for i in range(len(word)):
            if i == 0:
                # This is the first letter so also check the left is clear
                if col - 1 > -1 and grid[row][col - 1] != '#':
                    return False 
        
            if i == len(word) - 1:
                # This is the last letter so also check the right is clear
                if col + i + 1 < 21:
                    #print("Last letter (" + word[i] + ") check for word " + word + " has square " + grid[row][col + i + 1])
                    if grid[row][col + i + 1] != '#':
                        return False 
                           
            if not is_clear_horizontal(word[i], row, col + i):
                return False
            
        return True

    # Function to check if a word can be placed vertically at a specific position
    def can_place_vertically(word, row, col):
        if row + len(word) > 21:
            return False
        
        # Check each letter and the surrounding cells
        for i in range(len(word)):
            if i == 0:
                # This is the first letter so also check above is clear
                if row - 1 > -1 and grid[row - 1][col] != '#':
                    return False 
        
            if i == len(word) - 1:
                # This is the last letter so also check below is clear
                if row + i + 1 < 21:
                    #print("Last letter (" + word[i] + ") check for word " + word + " has square " + grid[row + i + 1][col])
                    if grid[row + i + 1][col] != '#':
                        return False 
                      
            if not is_clear_vertical(word[i], row + i, col):
                return False
        return True

    # Place words on the grid
    placed_words = []

    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            row = random.randint(0, 20)
            col = random.randint(0, 20)
            if can_place_horizontally(word, row, col):
                for i in range(len(word)):
                    grid[row][col + i] = word[i]
                placed_words.append((word, (row * 21) + col + 1, 'across'))
                placed = True
            elif can_place_vertically(word, row, col):
                for i in range(len(word)):
                    grid[row + i][col] = word[i]
                placed_words.append((word, (row * 21) + col + 1, 'down'))
                placed = True
            attempts += 1

    # Convert grid to a printable string
    crossword = '\n'.join([''.join(row) for row in grid])
    return crossword, placed_words

# Example usage
word_list = [
    'SEPOSI', 'TAHU', 'NASI', 'GORENG', 'ENAK', 'MENGIRIS', 'ROTI',
    'KEJU', 'MERICA', 'RASA', 'MANIS', 'GULA', 'TELUR', 'LAPAR',
    'MASAK', 'MAKAN', 'MAKANAN', 'PISANG', 'BABI', 'BAYAM',
    'MAU', 'MEMASAN', 'PANAS', 'DINGIN', 'DAGING', 'GARPU', 'SENDOK',
    'MEJA', 'PIRING', 'IKAN', 'CABAI', 'GARAM', 'GURIH', 'BAWANG',
    'AYAM', 'BUMBU', 'ASIN', 'ROTI', 'SARAPAN', 'SAYURAN', 'SAMBAL',
    'KENTANG', 'PISAU', 'MANGKUK', 'KOMPOR', 'WARUNG', 'MINUMAN',
    'MINUM', 'GURITA', 'TANPA', 'BERDELAPAN'
    ]

crossword, placed_words = create_crossword(word_list)

# Print the metadata
print("Title: Food and eating out")
print("Author: by Stuart Allen")
print("Copyright: © 2024 Stuart Allen")
print("Date: " + str(datetime.date.today()))
print("\n")


# Print the crossword grid
print(crossword)

print("\n")

sorted_across = []
sorted_down = []

# Sort the words into order of the square they start in
placed_words.sort(key=lambda word: word[1])

# Reduce the starting squares to a sequential order
ordered_words = []

clue_number = 1
last_square = 0

# We need to order the words sequentially, but clues that start on the
# same square need to have the same clue number
for i in range(len(placed_words)):
    word, square, orientation = placed_words[i]  # Unpack the current tuple

    if (last_square == square):
        # This clue starts in the same square as the last so don't
        # increment the clue_number
        ordered_words.append((word, clue_number, orientation))
    else:
        ordered_words.append((word, clue_number, orientation))
        clue_number += 1
    
    last_square = square

# print(ordered_words)

for i in range(len(ordered_words)):
    word, square, orientation = ordered_words[i]  # Unpack the current tuple
    if (orientation) == 'across':
        sorted_across.append((word, square))

for i in range(len(ordered_words)):
    word, square, orientation = ordered_words[i]  # Unpack the current tuple
    if (orientation == 'down'):
        sorted_down.append((word, square)) 
    
# Print the updated positions of the words
for word, number in sorted_across:
    print(f"A{number}. {word}")

print("")

for word, number in sorted_down:
    print(f"D{number}. {word}")
