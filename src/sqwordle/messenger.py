"""messenger.py

This module handles sending and receiving messages to the WORDLE
game in the browser. This includes requesting the webpage,
automating the input of guesses determined by the MasterMind,
and sending the results of the previous guess (or the current game state)
back to the MasterMind. 

The messenger also keeps track of the game state including the current
round, letters present, whether the game has ended.

The messenger does not determine what the next guess ought to me.
"""
import typing as t
from dataclasses import dataclass

import sqwordle.settings as settings
from sqwordle.utils.driver import Driver


@dataclass
class GameState:

    turn: t.Optional[int] = 1
    present_letters: t.Optional[t.List[str]] = None
    first: t.Optional[str] = None
    second: t.Optional[str] = None
    third: t.Optional[str] = None
    fourth: t.Optional[str] = None
    fifth: t.Optional[str] = None

    def __post_init__(self):
        if not self.present_letters:
            self.present_letters = []

    def __repr__(self):
        return f"WORDLE {self.__class__.__name__}(turn={self.turn})"

    @property
    def game_finished(self) -> bool:
        if self.turn > 5:
            return True
        return False

    def increment_turn(self):
        self.turn += 1


class Messenger:
    """
    The messenger is a Selenium web bot.
    """

    driver = Driver.get_driver()
    gamestate = GameState()
    wordle_url = settings.WORDLE_URL

    @classmethod
    def play_wordle(cls):
        cls.driver.get(cls.wordle_url)

        while not cls.gamestate.game_finished:

            # get first guess from master mind
            print("getting next guess")

            # read game state
            print("sending gamestate to mastermind")

            # increment round
            cls.gamestate.increment_turn()
            print(cls.gamestate.turn)

        cls.driver.quit()
