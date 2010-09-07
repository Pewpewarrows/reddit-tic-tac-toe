# Quick utility functions for a tic-tac-toe game

from random import choice

# The core AI of the tic-tac-toe game, based on difficulty level.
# 0: randomly chooses a move and makes it
# 1: TODO: knows how to block a winning move, tries to set-up its own
# 2: unbeatable
def ai_move(ai_level, ai_pos, user_pos, board_size):
    if ai_level == 0:
        cur_board = ai_pos | user_pos
        # That class on bitwise operators finally comes in handy!
        # Pushing 1 over however many bits you want then subtracting
        # another 1 gives you an int whose value is all 1 bits.
        # XOR'ing this with the current board inverses it for free spots.
        empty_spaces = cur_board ^ ((1 << (board_size**2)) - 1)

        possible_moves = []
        for i, v in enumerate(int_to_bin(empty_spaces, board_size)):
            if v == '1':
                possible_moves.append(i)

        if len(possible_moves) > 0:
            move = choice(possible_moves)
            return int_to_bin((1 << (board_size**2 - move - 1)), board_size)
        else:
            return '0' * board_size**2
    elif ai_level == 1:
        pass
    elif ai_level == 2:
        pass

# Computes the move of the new_move bitmask string on top of the old
# board positions for this player.
def add_move(old_pos, new_move, board_size):
    new_pos = old_pos | int(new_move, 2)
    new_pos_bin = int_to_bin(new_pos, board_size)

    return new_pos, new_pos_bin

# Integer to binary bit-mask string, left-padded with zeroes to board size
def int_to_bin(x, board_size):
    bin_x = bin(x)[2:]

    # Left-pad our bitmask
    while len(bin_x) < board_size**2:
        bin_x = '0' + bin_x

    return bin_x

# A move is illegal if the bitwise AND of it with the current board is 
# greater than 1. The only illegal move is that on an already-occupied
# space, which would yeild a 1 when AND'ed together.
def is_legal_move(x_pos, o_pos, move):
    return (x_pos & o_pos & int(move, 2) == 0)

def game_over(cur_pos):
    # In the interest of time, I'm hard-coding all 3x3 win conditions
    win_pos = [7, 56, 73, 84, 146, 273, 292, 448]

    for w in win_pos:
        if (w & cur_pos) == w:
            return True

    return False
