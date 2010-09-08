"""The application's model objects"""
from tictactoe.model.meta import Session, Base

from tictactoe.model.game import Game


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

