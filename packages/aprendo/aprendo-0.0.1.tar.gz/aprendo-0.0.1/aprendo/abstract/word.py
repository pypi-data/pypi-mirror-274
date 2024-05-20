from abc import ABC, abstractmethod

class Word(ABC):
    @abstractmethod
    def get_word(self):
        pass

    @abstractmethod
    def get_translation(self):
        pass

    @abstractmethod
    def get_example(self):
        pass
