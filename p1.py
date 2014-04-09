import numpy as np
pairs = [(a.split(), b.split()) for (a,b) in [('the dog','de hond'),('the cat','de kat'),('a dog','een hond'),('a cat','een kat')]]

# doublecounter : f -> e -> val
t = {}
count = {}

vocf = Counter([b for a,_ in pairs for b in a])
voce = Counter([b for _,a in pairs for b in a])

epsilon = 2.0 # float!!!

# initialize uniform
for f in vocf:
    t[f] = Counter()
    for e in voce:
        t[f][e] = 1.0/len(voce)

perplexity = float('inf')
while perplexity > 1:
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
    
    perplexity = 0
    for (fs, es) in pairs:
        p = 0
        for f in fs:
            for e in es:
                p += t[f][e]
        p = (epsilon/(len(fs)**len(es))) * p
        perplexity += np.log2(p)
    perplexity *= -1
    print 2**perplexity
