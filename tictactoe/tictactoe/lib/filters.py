def move_to_img(move):
    move = move.lower()

    if move == 'x':
        return '<img src="/static/images/x-symbol.png"/>'
    elif move == 'o':
        return '<img src="/static/images/o-symbol.png"/>'
    else:
        return '<input type="submit" class="move-button" value=" "/>'

def i_to_b(num):
    from tictactoe.lib.game import int_to_bin
    return int_to_bin(int(num), 3) # hardcoded because I don't give a damn
