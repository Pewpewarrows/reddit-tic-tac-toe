import logging
import random

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from tictactoe.lib.base import BaseController, render, Session
from tictactoe.model import Game

log = logging.getLogger(__name__)

class GameController(BaseController):

    def __before__(self):
        self.game_q = Session.query(Game)

    def index(self):
        return render('/game/index.mako')

    def new_ai(self):
        # For now, just start an AI game and store it in session,
        # which is what we'll end up doing for AI games pre-save.
        # We'll be hitting the database on versus game starts though,
        # or if the user decides to 'save' an AI game.
        
        # If there's a POST request, we're already mid-game.

        # New games for now randomly pick between you or AI starting
        coin_toss = random.randrange(2)

        # Only supporting same-sized edges boards for now
        board_size = 3
        x_pos_bin = '000000000'
        o_pos_bin = '000000000'
        x_pos = 0
        y_pos = 0

        # TODO: actually implement difficulty levels
        # AI difficulty from 0..2, with 0 being least difficult
        ai_level = 0

        # 0: AI goes first, 1: You go first
        # X is for the player going first
        if coin_toss == 0:
            x_pos |= int('000010000', 2)
            x_pos_bin = bin(x_pos)[2:]

            while len(x_pos_bin) < board_size**2:
                x_pos_bin = '0' + x_pos_bin

        x_pos = int(x_pos_bin, 2)
        o_pos = int(o_pos_bin, 2)

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

        return render('/game/new.mako')

    def new_versus(self):
        # Create a new Human Versus game ID and redirect to it
        pass
