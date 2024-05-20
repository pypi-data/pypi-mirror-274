from .verb import Verb


class RegularVerb(Verb):
    def __init__(self, word, translation):
        super().__init__(word, translation)
        self.base = self.remove_stem()

    @classmethod
    def factory(cls, word, translation):
        from .er_regular_verb import ERRegularVerb
        from .ir_regular_verb import IRRegularVerb
        from .ar_regular_verb import ARRegularVerb

        if word.endswith('ar'):
            return ARRegularVerb(word, translation)
        elif word.endswith('er'):
            return ERRegularVerb(word, translation)
        elif word.endswith('ir'):
            return IRRegularVerb(word, translation)
        else:
            return None
        
    def remove_stem(self):
        return self.word[:-2]
    
    def get_ending(self):
        return self.word[-2:]
    
    def db_factory(db_row):
        word = db_row[1]
        translation = db_row[2]
        return RegularVerb.factory(word, translation)
