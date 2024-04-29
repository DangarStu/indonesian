#!/usr/local/bin/python
import random

def create_crossword(words):
    # Create an empty grid
    grid = [['#' for _ in range(21)] for _ in range(21)]

    # Sort words by length in descending order
    words.sort(key=lambda x: len(x), reverse=True)

    # Function to check if a word can be placed horizontally at a specific position
    def can_place_horizontally(word, row, col):
        if col + len(word) > 21:
            return False
        for i, letter in enumerate(word):
            if grid[row][col + i] != '#' and grid[row][col + i] != letter:
                return False
        return True

    # Function to check if a word can be placed vertically at a specific position
    def can_place_vertically(word, row, col):
        if row + len(word) > 21:
            return False
        for i, letter in enumerate(word):
            if grid[row + i][col] != '#' and grid[row + i][col] != letter:
                return False
        return True

    # Function to place a word horizontally at a specific position
    def place_horizontally(word, row, col):
        for i, letter in enumerate(word):
            grid[row][col + i] = letter
        return (row, col)

    # Function to place a word vertically at a specific position
    def place_vertically(word, row, col):
        for i, letter in enumerate(word):
            grid[row + i][col] = letter
        return (row, col)

    # Place the words and update their positions in the placed_words list
    placed_words = []
    for word in words:
        placed = False
        while not placed:
            row = random.randint(0, 20)
            col = random.randint(0, 20)
            if can_place_horizontally(word, row, col):
                position = place_horizontally(word, row, col)
                placed_words.append((word, position[0], position[1]))
                placed = True
            elif can_place_vertically(word, row, col):
                position = place_vertically(word, row, col)
                placed_words.append((word, position[0], position[1]))
                placed = True

    # Convert grid to a printable string
    crossword = '\n'.join([''.join(row) for row in grid])
    return crossword, placed_words

# Example usage
word_list = ['PYTHON', 'CROSSWORD', 'GRID', 'ALGORITHM', 'PROGRAMMING', 'PUZZLE']
crossword, placed_words = create_crossword(word_list)

# Print the crossword grid
print(crossword)

# Print the updated positions of the words
print("Words placed with updated positions:")
for word, row, col in placed_words:
    print(f"{word} placed at row {row}, column {col}")
