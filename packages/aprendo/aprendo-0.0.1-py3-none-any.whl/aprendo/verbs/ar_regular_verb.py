from .regular_verb import RegularVerb

class ARRegularVerb(RegularVerb):
    def __init__(self, word, translation):
        super().__init__(word, translation)
        self.ending = 'ar'

    def get_conjugation(self, pronoun):
        if pronoun == 'yo':
            return self.base + 'o'
        elif pronoun == 'tu':
            return self.base + 'as'
        elif pronoun == 'el':
            return self.base + 'a'
        elif pronoun == 'nosotros':
            return self.base + 'amos'
        elif pronoun == 'vosotros':
            return self.base + 'ais'
        elif pronoun == 'ellos':
            return self.base + 'an'
        else:
            return 'Unknown pronoun'
        
    def get_translation(self):
        return self.translation
    
    def get_example(self):
        pass