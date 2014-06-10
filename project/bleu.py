from math import exp, log

def ngrams(s, n):
	return [" ".join(s[i:i + n]) for i in range(len(s) - n + 1)]

def precision(gold, out):
	if not gold or not out:
		return 1
	return float(len(set(gold) & set(out))) / float(len(set(out)))


def bleu(gold, out):
	mylog = lambda x: log(x) if x else -float('inf')
	bp = min(1, float(len(out)) / float(len(gold)))
	ps = [precision(ngrams(gold, n), ngrams(out, n)) for n in [1, 2, 3, 4]]
	return bp * exp((mylog(ps[0]) +
					 mylog(ps[1]) +
					 mylog(ps[2]) + 
					 mylog(ps[3]) ) / 4)
