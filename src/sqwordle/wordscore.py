"""wordscore.py

This module provides the dataclass used to represent each word and
a WordScorer class to instantiate and score all Word objects.
"""
import pickle
import typing as t
from dataclasses import dataclass

import sqwordle.settings as settings
import sqwordle.utils.words as candidate


@dataclass
class Word:
    """Each word in SQWORLD is comprised of 5 (possibly repeating)
    letters. These letters (and whether or not they are duplicated
    in the word) determine the score the word is given.
    """

    word: str
    score: t.Optional[int] = None

    def __post_init__(self):
        self.first = self.word[0]
        self.second = self.word[1]
        self.third = self.word[2]
        self.fourth = self.word[3]
        self.fifth = self.word[4]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.word}, score={self.score})"


class WordScorer:
    """
    WordScorer handles all the setup for scoring possible 5 letter words.

    This involves reading in common words from a text file, instantiating
    Word objects from each string representing a word, and determining
    the appropriate score to give to each Word.
    """

    # The class level attributes hold constant data used to score words
    highest_value_letters = "e a i o n r t l s u".split()
    higher_value_letters = "d g".split()
    high_value_letters = "b c m p".split()
    mid_value_letters = "f h v w y".split()
    low_value_letters = ["k"]
    lower_value_letters = "j x".split()
    lowest_value_letters = "q z".split()

    # keys of hashtable = letter, value = score
    ten_points = dict.fromkeys(highest_value_letters, 10)
    eight_points = dict.fromkeys(higher_value_letters, 8)
    five_points = dict.fromkeys(high_value_letters, 5)
    four_points = dict.fromkeys(mid_value_letters, 4)
    three_points = dict.fromkeys(low_value_letters, 3)
    two_points = dict.fromkeys(lower_value_letters, 2)
    one_point = dict.fromkeys(lowest_value_letters, 1)

    letter_point_map = {
        **ten_points,
        **eight_points,
        **five_points,
        **four_points,
        **three_points,
        **two_points,
        **one_point,
    }

    _common_five_letter_words = set()
    _all_unscored_words: t.List[str] = candidate.words
    _all_scored_words: t.List[Word] = []

    @classmethod
    def parse_common_word_file(
        cls, location: t.Optional[str] = settings.COMMON_WORDS_PATH
    ) -> None:
        """Open a file of words and parse it as a list.

        :param locations: a relative file path to the list of words
        """
        with open(location) as word_file:
            line = word_file.readline().rstrip()
            common_words = line.split()
            cls._common_five_letter_words = set(common_words)

    @classmethod
    def _sort_words_by_score(cls) -> None:
        cls._all_scored_words = sorted(
            cls._all_scored_words, key=lambda word: word.score
        )

    @classmethod
    def _determine_letter_value_in_current_word(
        cls, letter: str, seen: set
    ) -> int:
        """Determine the value of a current letter for a given word
        based on its value in our hashtable and whether it is unique."""
        if letter not in seen:
            seen.add(letter)
            return cls.letter_point_map[letter]
        return 1

    @classmethod
    def score_word(cls, word: Word) -> None:
        """
        My method for determining how valuable a letter ought to be
        is simply by taking the scoring rules of Scrable, and reversing
        them. Letters like 'a e i o u' are common and thus score few
        points in Scrable. For WORDLE, these are the most valuable as
        they ought to reveal the most information about the mystery word.

        Scoring a word involves not only looking up its value in
        our hashtable of letters to their values, but also penalizing
        words for duplicate letters. This is done by giving the duplicate
        letter a value of 1. Words are also rewarded for being a 'common'
        word.

        :param word: a Word with an initialized score property of None.
        """

        seen = set()
        word_score = 0

        word_score += cls._determine_letter_value_in_current_word(
            word.first, seen
        )
        word_score += cls._determine_letter_value_in_current_word(
            word.second, seen
        )
        word_score += cls._determine_letter_value_in_current_word(
            word.third, seen
        )
        word_score += cls._determine_letter_value_in_current_word(
            word.fourth, seen
        )
        word_score += cls._determine_letter_value_in_current_word(
            word.fifth, seen
        )

        if word.word in cls._common_five_letter_words:
            word_score += 11

        word.score = word_score

    @classmethod
    def score_all_words(cls) -> None:
        """Determine the overall score for each unscored Word and bind
        this score to the the score property.
        """
        # set word score property
        for unscored_word in cls._all_unscored_words:
            word = Word(unscored_word)
            cls.score_word(word)
            cls._all_scored_words.append(word)

        cls._sort_words_by_score()

    @classmethod
    def dump_word_scores_to_disk(
        cls, location: t.Optional[str] = settings.SCORED_WORDS_DUMP
    ) -> None:
        """Pickle all scored Words to a binary file."""
        with open(location, "wb") as pickle_file:
            pickle.dump(
                cls._all_scored_words,
                pickle_file,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

    @classmethod
    def read_word_scores_from_disk(
        cls, location: t.Optional[str] = settings.SCORED_WORDS_DUMP
    ) -> None:
        """Unpickle a binary file of scored Words and bind them to class."""
        with open(location, "rb") as pickle_file:
            cls._all_scored_words = pickle.load(pickle_file)
