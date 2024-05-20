from ..abstract.word import Word
from abc import ABC, abstractmethod
from .constants import SPANISH_PRONOUNS

class Verb(Word, ABC) :
    def __init__(self, word, translation):
        self.word = word
        self.translation = translation
        self.pronouns = SPANISH_PRONOUNS

    def get_word(self):
        return self.word

    @abstractmethod
    def get_translation(self):
        return self.translation

    @abstractmethod
    def get_example(self):
        pass

    @abstractmethod
    def get_conjugation(self):
        pass

   