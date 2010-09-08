# Quick utility functions for a tic-tac-toe game

# This really should just be a class since I'm passing around these variables
# over and over again, but whatever.

from random import choice

# The core AI of the tic-tac-toe game, based on difficulty level.
# 0: randomly chooses a move and makes it
# 1: knows how to block a winning move, otherwise still random
# 2: unbeatable
def ai_move(ai_level, ai_pos, user_pos, board_size):
    if ai_level == 0:
        return ai_random_move(ai_pos, user_pos, board_size)
    elif ai_level == 1:
        move = ai_block_move(ai_pos, user_pos, board_size)
        if move:
            return move

        return ai_random_move(ai_pos, user_pos, board_size)
    elif ai_level == 2:
        move = ai_block_move(ai_pos, user_pos, board_size)
        if move:
            return move

        # Really the only difference is that instead of random,
        # we attempt an aggressive move, which includes never 
        # choosing a side over a corner in early-game.
        move = ai_aggro_move(ai_pos, user_pos, board_size)
        if move:
            return move

        # Shouldn't ever get here, just in case
        return ai_random_move(ai_pos, user_pos, board_size)

def ai_random_move(ai_pos, user_pos, board_size):
    cur_board = ai_pos | user_pos
    # That class on bitwise operators finally comes in handy!
    # Left shifting 1 over however many bits you want then subtracting
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

def ai_block_move(ai_pos, user_pos, board_size):
    cur_board = ai_pos | user_pos
    ai_pos = int_to_bin(ai_pos, board_size)
    user_pos = int_to_bin(user_pos, board_size)

    for r in range(board_size):
        user_row = user_pos[r * board_size : (r * board_size) + (board_size)]
        ai_row = ai_pos[r * board_size : (r * board_size) + (board_size)]
        if (bit_count(int(user_row, 2)) == 2) and (bit_count(int(ai_row, 2)) != 1):
            move = int(('1' * board_size), 2) ^ int(user_row, 2)
            move = ((r * board_size) * '0') + int_to_bin(move, board_size)[-3:]
            move += ((board_size**2 - len(move)) * '0')
            return move

    for c in range(board_size):
        user_col = ''
        ai_col = ''
        for i in range(board_size):
            user_col += user_pos[c + (i * board_size)]
            ai_col += ai_pos[c + (i * board_size)]

        if (bit_count(int(user_col, 2)) == 2) and (bit_count(int(ai_col, 2)) != 1):
            move_arr = int_to_bin((int(('1' * board_size), 2) ^ int(user_col, 2)), board_size)[-3:]
            move = ''
            for m in move_arr:
                mini_move = ('0' * c) + m
                move += mini_move + ('0' * (board_size - len(mini_move)))
            return move

    # TODO: eventually generate the cross block positions based on board size
    # For now, we have a dict of cross-win conditions and their blocking move
    cross_pos = {17: 256, 20: 64, 68: 16, 80: 4, 257: 16, 272: 1}
    user_pos_int = int(user_pos, 2)

    for x, v in cross_pos.items():
        if (x & user_pos_int) == x:
            if (cur_board & v) == 0:
                return int_to_bin(v, board_size)

    return None

def ai_aggro_move(ai_pos, user_pos, board_size):
    cur_board = ai_pos | user_pos
    # First check to see if we have any 2 in a row lined up already
    # TODO: this is identical to code above for blocking, abstract out
    cross_pos = {17: 256, 20: 64, 68: 16, 80: 4, 257: 16, 272: 1}

    for x, v in cross_pos.items():
        if (x & ai_pos) == x:
            if (cur_board & v) == 0:
                return int_to_bin(v, board_size)

    # Otherwise, go for a corner (playing the side early is the only
    # way for someone to double-trap you).
    corners = [256, 64, 4, 1]

    for c in corners:
        if (cur_board & c) == 0:
            return int_to_bin(c, board_size)

    return None

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
    if bit_count(int(move, 2)) > 1:
        return false

    return (x_pos & o_pos & int(move, 2) == 0)

def game_over(cur_pos):
    # In the interest of time, I'm hard-coding all 3x3 win conditions
    win_pos = [7, 56, 73, 84, 146, 273, 292, 448]

    for w in win_pos:
        if (w & cur_pos) == w:
            return True

    return False

# http://wiki.python.org/moin/BitManipulation
def bit_count(num):
    count = 0
    while (num):
        num &= num - 1
        count += 1

    return count
