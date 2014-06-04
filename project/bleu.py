def ngrams(s, n):
    return [s[i:i+n] for i in range(len(s)-n+1)]
def precision(gold, out):
    return float(len(set(gold) & set(out))) / float(len(set(out)))

def bleu(gold, out):
    bp = min(1, len(out)/len(gold))
    ps = [precision(ngrams(gold, n), ngrams(test, n)) for n in [1,2,3,4]]
    print ps
    return bp * ps[0] * ps[1] * ps[2] * ps[3] 