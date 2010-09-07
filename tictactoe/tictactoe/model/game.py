from sqlalchemy import Column, Unicode, Integer, Boolean
import string
from random import choice

from tictactoe.model.meta import Base

class Game(Base):
    __tablename__ = 'game'

    # Hash of 8 alphanumeric characters to serve as the URL as well
    # I think 218 trillion possible games is enough for now...
    id = Column(Unicode(8), primary_key=True)
    # Size of the game board
    size = Column(Integer)
    # Integer representation of both players' moves bitmask
    x_pos = Column(Integer)
    o_pos = Column(Integer)
    # True for human, False for AI
    versus = Column(Boolean)
    # TODO: password protection?

    def __init__(self, id='', size=3, x_pos=0, o_pos=0, versus=False):
        # I'm lazy, sue me
        if id == '':
            id = self.generate_hash

        self.id = id
        self.size = size
        self.x_pos = x_pos
        self.o_pos = o_pos
        self.versus = versus

    def __repr__(self):
        return "<Game('%s') " % self.id

    def generate_hash(self, length=8):
        allowed_chars = string.letters + string.digits
        return ''.join([choice(allowed_chars) for i in range(length)])
