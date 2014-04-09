
from translation import Translation
from collections import Counter

def loadCorpus():
	source = list(open('corpus.nl', 'r'))
	target = list(open('corpus.en', 'r'))
	return source, target

def runEM(source, target):
	t = Translation()
	count = Translation()
	total = Counter()
	for i in xrange(len(source)):
		e_s = target[i]
		f_s = source[i]
		total_s = Counter()
		for f in f_s:
			for e in e_s:
				if f in total_s:
					total_s[f] += t(f, e)
		for f in f_s:
			for e in e_s:
				new = t.get(f=f, e=e) / total_s[f]
				count.update(f=f, e=e, val=new)
				total[e] += new

	for e in

