from .regular_verb import RegularVerb

class ERRegularVerb(RegularVerb):
    def __init__(self, word, translation):
        super().__init__(word, translation)
        self.ending = 'er'

    def get_conjugation(self, pronoun):
        if pronoun == 'yo':
            return self.base + 'o'
        elif pronoun == 'tu':
            return self.base + 'es'
        elif pronoun == 'el':
            return self.base + 'e'
        elif pronoun == 'nosotros':
            return self.base + 'emos'
        elif pronoun == 'vosotros':
            return self.base + 'eis'
        elif pronoun == 'ellos':
            return self.base + 'en'
        else:
            return 'Unknown pronoun'
    
    def get_translation(self):
        return self.translation
    
    def get_example(self):
        pass

    