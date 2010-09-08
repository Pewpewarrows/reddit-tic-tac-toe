import logging
from random import randrange

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from tictactoe.lib.base import BaseController, render, Session
from tictactoe.lib.game import ai_move, add_move, int_to_bin, is_legal_move, game_over, bit_count
from tictactoe.model import Game

log = logging.getLogger(__name__)

class GameController(BaseController):

    def __before__(self):
        self.game_q = Session.query(Game)

    def index(self):
        return render('/game/index.mako')

    def new_ai_choose(self):
        return render('/game/diff.mako')

    def new_ai(self, diff):
        # For now, just start an AI game and store it in session,
        # which is what we'll end up doing for AI games pre-save.
        # We'll be hitting the database on versus game starts though,
        # or if the user decides to 'save' an AI game.

        # Only supporting same-sized edged boards for now
        board_size = 3
        x_pos_bin = '000000000'
        o_pos_bin = '000000000'
        x_pos = 0
        o_pos = 0
        finished = False
        message = ''

        # AI difficulty from 0..2, with 0 being least difficult
        if diff == 'easy':
            ai_level = 0
        elif diff == 'med':
            ai_level = 1
        elif diff == 'hard':
            ai_level = 2
        else:
            return redirect('/game/new/ai/')

        # An option to clear the session's game cache for a fresh start
        if 'reset' in request.POST and request.POST['reset'] == 'true':
            session.clear()
            session.save()
            return redirect('/game/new/ai/')

        # If there's a POST request or we see session variables from a
        # previous game, we're already mid-game.
        # TODO: if move and reset are both in POST, this breaks
        if ('move' in request.POST) or ('game' in session):
            board_size = session['size']
            x_pos = session['x_pos']
            o_pos = session['o_pos']
            user_side = session['user_side']
            ai_level = session['ai_level']
            finished = session['finished']
            message = session['message']
            x_pos_bin = int_to_bin(x_pos, board_size)
            o_pos_bin = int_to_bin(o_pos, board_size)

            if (not finished) and ('move' in request.POST):
                if is_legal_move(x_pos, o_pos, request.POST['move']):
                    if user_side == 'X':
                        x_pos, x_pos_bin = add_move(x_pos, request.POST['move'], board_size)
                        if game_over(x_pos):
                            finished = True
                            message = 'You win!'
                        else:
                            o_move = ai_move(ai_level, o_pos, x_pos, board_size)
                            o_pos, o_pos_bin = add_move(o_pos, o_move, board_size)
                            if game_over(o_pos):
                                finished = True
                                message = 'You lose!'
                    else:
                        o_pos, o_pos_bin = add_move(o_pos, request.POST['move'], board_size)
                        if game_over(o_pos):
                            finished = True
                            message = 'You win!'
                        else:
                            x_move = ai_move(ai_level, x_pos, o_pos, board_size)
                            x_pos, x_pos_bin = add_move(x_pos, x_move, board_size)
                            if game_over(x_pos):
                                finished = True
                                message = 'You lose!'

                    if not finished and (bit_count(x_pos | o_pos) == board_size**2):
                        finished = True
                        message = 'It\'s a tie!'
        else:
            # New games for now randomly pick between you or AI starting
            coin_toss = randrange(2)

            # 0: AI goes first, 1: You go first
            # X is for the player going first
            if coin_toss == 0:
                user_side = 'O'
                # Eventually use ai_move, for now assume always go center
                x_pos, x_pos_bin = add_move(x_pos, '000010000', board_size)
            else:
                user_side = 'X'

        x_pos = int(x_pos_bin, 2)
        o_pos = int(o_pos_bin, 2)

        session['game'] = True
        session['size'] = board_size
        session['x_pos'] = x_pos
        session['o_pos'] = o_pos
        session['user_side'] = user_side
        session['ai_level'] = ai_level
        session['finished'] = finished
        session['message'] = message
        session.save()

        positions = []
        for i in range(board_size):
            positions.append([])

            for j in range(board_size):
                if x_pos_bin[(i*board_size)+j] == '1':
                    positions[i].append('X')
                elif o_pos_bin[(i*board_size)+j] == '1':
                    positions[i].append('O')
                else:
                    positions[i].append('')

        # Absolutely no idea if this is proper or not, but I'd rather
        # not fish through the entire function for declared context
        # variables, so I'm going with sticking them all at the end.
        c.board_size = board_size
        c.positions = positions
        c.user_size = user_side
        c.finished = finished
        c.message = message

        return render('/game/new.mako')

    def new_versus(self):
        # Create a new Human Versus game ID and redirect to it
        pass
