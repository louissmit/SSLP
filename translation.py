from collections import Counter

class Translation:
    def __init__(self, vocab_e, vocab_f):
        if not vocab_e or not vocab_f:
            raise Exception("Supply vocabulary")
        self.vocab_e = vocab_e
        self.vocab_f = vocab_f
        self.es = len(vocab_e)
        self.fs = len(vocab_f)
        self.table = {}
    
    def get(self, e, f):
        return 1.0/self.fs if not e in self.table else table[e]
    
    def update(self, e, f, val):
        self.table[e][f] = val
