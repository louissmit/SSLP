import numpy as np
from collections import Counter
from decimal import Context, Decimal
# pairs = [(a.split(), b.split()) for (a,b) in [('the dog','de hond'),('the cat','de kat'),('a dog','een hond'),('a cat','een kat')]]
from IBM import getViterbiAlignment

def loadCorpus():
    source = list(open('corpus_1000.nl', 'r'))
    target = list(open('corpus_1000.en', 'r'))
    return source, target

source, target = loadCorpus()

def corpus(n=None):
    """ An iterator of pairs """ 
    n = n or len(source)
    for i in xrange(n):
        yield source[i].split(),target[i].split()

def round_dc(dc, n=0):
    """ Rounds a dictionary of Counters """
    for k,v in dc.iteritems():
        new = Counter()
        for i,c in v.iteritems():
            c = round(c, n)
            if c:
                new[i] = c
        dc[k] = new
    return dc

def translate(pairs, stability=1):
    """ Builds IBM1 translation table, doing EM until the perplexity difference is < `stability` """
    # doublecounter : f -> e -> val
    t = {}
    count = {}

    vocf = Counter([b for a,_ in pairs for b in a])
    voce = Counter([b for _,a in pairs for b in a])

    epsilon = 1.0 # float!!!
#     epsilon = sum([len(x) for x,_ in pairs]) / float(len(pairs))
    print 'epsilon:', epsilon

    # initialize uniform
    for f in vocf:
        t[f] = Counter()
        for e in voce:
            t[f][e] = 1.0/len(voce)

    perplexity = float('inf')
    stable = False
    while not stable:
        for f in vocf:
            count[f] = Counter()
        total = Counter()

        for (fs, es) in pairs:
            total_s = Counter()
            for f in fs:
                total_s[f] = sum(t[f].values())
            for f in fs:
                for e in es:
                    count[f][e] += t[f][e] / total_s[f]
                    total[e] += t[f][e] / total_s[f]

        for e in voce:
            for f in vocf:
                t[f][e] = count[f][e] / total[e]
                if not t[f][e]:
                    del t[f][e]
        
        log_pp = 0
        for (fs, es) in pairs:
            p = 0.0
            for f in fs:
                for e in es:
                    p += t[f][e]
            p *= (epsilon/(len(fs)**len(es)))
            log_pp += np.log2(p)
        old_perplexity = Decimal(perplexity)
        perplexity = Context().power(2, Decimal(-log_pp))#2**(-perplexity)
        stable = abs(old_perplexity - perplexity) < stability
        print 'perplexity:', perplexity, ('stable' if stable else 'not stable')
        
    return t
    
# Example uses:
# round_dc(translate(pairs))
t = translate([a for a in corpus(100)], 10000)
getViterbiAlignment(source, target, t)


