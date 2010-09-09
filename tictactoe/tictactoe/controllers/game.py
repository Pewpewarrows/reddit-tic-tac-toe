import logging
from random import randrange

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

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
        session.clear()
        session.save()
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
        c.user_side = user_side
        c.finished = finished
        c.message = message
        c.this_url = request.environ.get('PATH_INFO')

        if request.is_xhr:
            return self.json(positions)

        return render('/game/new.mako')

    def new_versus(self):
        # Create a new Human Versus game ID and redirect to it
        game = Game(versus=True)
        game_id = game.id
        Session.add(game)
        Session.commit()

        return redirect('/game/cont/%s/' % game_id)

    def cont_game(self, id):
        # Continue an existing Human Versus game
        game = self.game_q.filter_by(id=id).first()
        if not game:
            return redirect('/')

        message = ''
        user_side = ''
        finished = False
        board_size = game.size
        x_pos = game.x_pos
        o_pos = game.o_pos
        x_pos_bin = int_to_bin(x_pos, board_size)
        o_pos_bin = int_to_bin(o_pos, board_size)

        if 'move' in request.POST:
            if 'user_side' in session:
                user_side = session['user_side']
            elif user_side == '':
                # Determine your side by the person whose turn it should be
                # Note: I have no idea what security issues this raises
                # should one user maliciously and purposfully clear their
                # cookies.
                if bit_count(x_pos) <= bit_count(o_pos):
                    user_side = 'X'
                else:
                    user_side = 'O'
                session['user_side'] = user_side
                session.save()

            if (not game_over(x_pos)) and (not game_over(o_pos)) and is_legal_move(x_pos, o_pos, request.POST['move'], user_side):
                if user_side == 'X':
                    x_pos, x_pos_bin = add_move(x_pos, request.POST['move'], board_size)
                    game.x_pos = x_pos
                    Session.commit()
                else:
                    o_pos, o_pos_bin = add_move(o_pos, request.POST['move'], board_size)
                    game.o_pos = o_pos
                    Session.commit()

        if game_over(x_pos):
            finished = True
            if user_side == 'X':
                message = 'You win!'
            elif user_side == 'O':
                message = 'You lose!'
        elif game_over(o_pos):
            finished = True
            if user_side == 'O':
                message = 'You win!'
            elif user_side == 'X':
                message = 'You lose!'
        elif bit_count(x_pos | o_pos) == (board_size**2):
            finished = True
            message = 'It\'s a tie!'

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

        c.board_size = board_size
        c.positions = positions
        c.user_side = user_side
        c.finished = finished
        c.message = message
        c.this_url = request.environ.get('PATH_INFO')
        # c.this_url = url.current(qualified=False)

        if request.is_xhr:
            return self.json(positions)
        
        return render('/game/continue.mako')

    @jsonify
    def json(self, data):
        return dict(result=data)

    @jsonify
    def long_poll(self, id):
        from datetime import datetime
        from time import sleep

        start = datetime.now()

        if 'my_board' in request.POST:
            my_board = request.POST['my_board']
            my_board = int(my_board, 2)
        else:
            return ''

        game = self.game_q.filter_by(id=id).first()

        while True:
            Session.refresh(game)
            if not game:
                return ''

            board_size = game.size
            x_pos = game.x_pos
            o_pos = game.o_pos
            cur_board = x_pos | o_pos
            data = {}

            if cur_board > my_board:
                x_pos_bin = int_to_bin(x_pos, board_size)
                o_pos_bin = int_to_bin(o_pos, board_size)

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

                data['result'] = positions

            if bit_count(cur_board) == (board_size**2):
                data['message'] = 'It\'s a tie!'

            if game_over(x_pos):
                data['message'] = 'X Wins!'
            elif game_over(o_pos):
                data['message'] = 'O Wins!'

            if len(data) > 0:
                return data
            
            sleep(1)

            delta = datetime.now() - start
            if delta.seconds >= 30:
                return {'again': True}

        return ''
