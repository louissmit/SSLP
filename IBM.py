
from translation import Translation
from collections import Counter
import numpy as np

def loadCorpus():
	source = list(open('corpus.nl', 'r'))
	target = list(open('corpus.en', 'r'))
	return source, target

def runEM(source, target, alpha):
	t = Translation()
	perplexity = 1000
	while perplexity > alpha:
		count = Translation()
		total = Counter()
		for i in xrange(len(source)):
			e_s = target[i]
			f_s = source[i]
			total_s = Counter()
			for f in f_s:
				for e in e_s:
					if f in total_s:
						total_s[f] += t.get(f=f, e=e)
			for f in f_s:
				for e in e_s:
					new = t.get(f=f, e=e) / total_s[f]
					count.update(f=f, e=e, val=new)
					total[e] += new

		t.normalize(count, total)
		perpexity = 0
		for i in xrange(0, len(source)):
			e_s = target[i]
			f_s = source[i]
			perpexity += np.log2(p(e_s, f_s))
		perplexity *= -1
		print perpexity

