def move_to_img(move):
    move = move.lower()

    if move == 'x':
        return '<img src="/static/images/x-symbol.png"/>'
    elif move == 'o':
        return '<img src="/static/images/o-symbol.png"/>'
    else:
        return move

