#!/usr/local/bin/python
import random

def create_crossword(words):
    # Create an empty grid
    grid = [[' ' for _ in range(21)] for _ in range(21)]

    # Sort words by length in descending order
    words.sort(key=lambda x: len(x), reverse=True)

    # Helper function to check cells around a given position
    # Only needs to be clear to left or right if vertical
    # and up and down if horizontal
    # Additionally:
    # If vertical the first letter must be clear above and
    # the last letter must be clear below
    # If horizonal the first letter must be clear to the left
    # and the last letter must be clear to the right.
    def is_clear_side_to_side(row, col):
        # Check cell is clear side to side
        for c in range(max(0, col - 1), min(21, col + 2)):
            if grid[row][c] != ' ':
                return False
        return True
    
    def is_clear_up_and_down(row, col):
        # Check cell is clear above and below
        for r in range(max(0, row - 1), min(21, row + 2)):
            if grid[r][col] != ' ':
                return False
        return True
    
    # Function to check if a word can be placed horizontally at a specific position
    def can_place_horizontally(word, row, col):
        if col + len(word) > 21:
            return False
        # Check each letter and the surrounding cells
        for i in range(len(word)):
            if not is_clear_up_and_down(row, col + i):
                return False
        return True

    # Function to check if a word can be placed vertically at a specific position
    def can_place_vertically(word, row, col):
        if row + len(word) > 21:
            return False
        # Check each letter and the surrounding cells
        for i in range(len(word)):
            if not is_clear_side_to_side(row + i, col):
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
                placed_words.append((word, 'Horizontal', row, col))
                placed = True
            elif can_place_vertically(word, row, col):
                for i in range(len(word)):
                    grid[row + i][col] = word[i]
                placed_words.append((word, 'Vertical', row, col))
                placed = True
            attempts += 1

    # Convert grid to a printable string
    crossword = '\n'.join([''.join(row) for row in grid])
    return crossword, placed_words

# Example usage
word_list = ['ROTI', 'KEJU', 'MERICA', 'RASA', 'MANIS', 'GULA', 'TELUR', 'LAPAR', 'MASAK', 'MAKAN', 'MAKANAN', 'PISANG', 'BABI']
crossword, placed_words = create_crossword(word_list)

# Print the crossword grid
print(crossword)

# Print the updated positions of the words
print("Words placed with updated positions:")
for word, orientation, row, col in placed_words:
    print(f"{word} placed {orientation} at row {row}, column {col}")

