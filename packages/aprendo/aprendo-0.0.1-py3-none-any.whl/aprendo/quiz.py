import datetime
import json
from .verbs import RegularVerb
from .nouns import Noun
from .abstract.word import Word
from .db import VerbsDB, NounsDB 
import questionary
import random
import unicodedata

class Quiz():

    def __init__(self):
        self.tracking = {}
        self.asked_questions = set()

    def _select_unique_word(self, word_list, cls):
        word = None
        while word is None or word.word in self.asked_questions:
            word = Noun.db_factory(random.choice(word_list)) if cls == Noun else RegularVerb.db_factory(random.choice(word_list))
        self.asked_questions.add(word.word)
        return word

    def _ask_question(self, word, word_type, language='random'):
        # Ask for the English translation
        if language == 'en':
            correct = self.ask_english_question(word, word_type)
        elif language == 'es':
            correct = self.ask_spanish_question(word, word_type)
        else:
            # get random language
            if random.choice([True,False]):
                return self._ask_question(word, word_type, 'en')
            else:
                return self._ask_question(word, word_type, 'es')

        if correct:
            print("Correct!")
        else:
            if language == 'en':
                print(f"Wrong! The correct English translation is: {word.translation}")
            else :
                print(f"Wrong! The correct Spanish translation is: {word.word}")

    def ask_spanish_question(self, word, word_type):
        question = f"What is the Spanish translation of the English {word_type}: {word.translation}?"
        answer = questionary.text(question).ask()
        correct = self._compare_with_or_without_accents(answer, word.word)
        self.tracking[question] = {'given_answer': answer, 'correct_answer': word.word, 'correct': correct}
        return correct
    
    def ask_english_question(self, word, word_type):
        question = f"What is the English translation of the Spanish {word_type}: {word.word}?"
        answer = questionary.text(question).ask()
        correct = self._compare_with_or_without_accents(answer, word.translation)
        self.tracking[question] = {'given_answer': answer, 'correct_answer': word.translation, 'correct': correct}
        return correct
    
    def _compare_with_or_without_accents(self, str1, str2):
        normalized_str1 = unicodedata.normalize('NFKD', str1).casefold()
        normalized_str2 = unicodedata.normalize('NFKD', str2).casefold()
        
        stripped_str1 = ''.join(c for c in normalized_str1 if not unicodedata.combining(c))
        stripped_str2 = ''.join(c for c in normalized_str2 if not unicodedata.combining(c))
        
        return stripped_str1 == stripped_str2

    def test_regular_verb(self, number_of_questions):
        verbs = VerbsDB().get_all_verbs()
        for _ in range(number_of_questions):
            verb : RegularVerb = self._select_unique_word(verbs, RegularVerb)
            self._ask_question(verb, "verb")

    def test_noun(self, number_of_questions):
        nouns = NounsDB().get_all_nouns()
        for _ in range(number_of_questions):
            noun : Noun = self._select_unique_word(nouns, Noun)
            self._ask_question(noun, "noun")

    def test(self, number_of_questions):
        self.test_regular_verb(number_of_questions)
        self.test_noun(number_of_questions)
        
    def get_tracking(self):
        return self.tracking
    
    def tracking_to_csv(self):
        import csv
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f'aprendo_quiz_{date}.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Question', 'Given Answer', 'Correct Answer', 'Correct'])
            for key, value in self.tracking.items():
                writer.writerow([key, value['given_answer'], value['correct_answer'], value['correct']])
    
    def print_tracking(self) :
        print(json.dumps(self.get_tracking(), indent=4))

