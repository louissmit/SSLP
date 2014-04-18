import numpy as np
import re
from collections import Counter
import pickle
from decimal import Context, Decimal
# pairs = [(a.split(), b.split()) for (a,b) in [('the dog','de hond'),('the cat','de kat'),('a dog','een hond'),('a cat','een kat')]]

def loadCorpus(flip=False):
	source = list(open('corpus_1000.nl', 'r'))
	target = list(open('corpus_1000.en', 'r'))
	if flip:
		return target, source
	else:
		return source, target


def corpus(n=None, flip=False):
	""" An iterator of pairs """
	source, target = loadCorpus(flip)
	n = n or len(source)
	for i in xrange(n):
		yield source[i].split(), ['NULL']+target[i].split()

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

def translate(pairs, n=20):
	""" Builds IBM1 translation table, doing EM until the perplexity difference is < `stability` """
	t = {}
	count = {}

	vocf = Counter([b for a,_ in pairs for b in a])
	voce = Counter([b for _,a in pairs for b in a])

	epsilon = 1.0
	alpha = 0.00001
	v = 100000
	print 'epsilon:', epsilon

	# initialize uniform
	for f in vocf:
		t[f] = Counter()
		for e in voce:
			t[f][e] = 1.0/len(voce)

	i = 0
	while i < n:
		#initialize count and total to 0
		for f in vocf:
			count[f] = Counter()
		total = Counter()

		# normalization
		for (fs, es) in pairs:
			total_s = Counter()
			for f in fs:
				for e in es:
					total_s[f] += t[f][e]
			#collect counts
			for f in fs:
				for e in es:
					count[f][e] += t[f][e] / total_s[f]
					total[e] += t[f][e] / total_s[f]

		# estimate probabilities
		for e in voce:
			for f in vocf:
				t[f][e] = (count[f][e] + alpha) / (total[e] + v*alpha)

		# calculate log perplexity
		log_pp = 0
		for (fs, es) in pairs:
			p = 0.0
			for f in fs:
				for e in es:
					p += t[f][e]
			p *= (epsilon/((len(es)+1)**len(fs)))
			log_pp += np.log2(p)
		print 'log perplexity:', -log_pp
		i += 1

	return t


def getViterbiAlignment(pairs, t):
	"""
	Gets viterbi alignment
	@param pairs:
	@param t: Translation model
	"""
	all_alignments = []
	for (f_s, e_s) in pairs:
		alignments = [[] for _ in xrange(len(e_s))]
		for j, f in enumerate(f_s):
			max = -1
			max_i = -1
			for i, e in enumerate(e_s):
				if t[f][e] > max:
					max = t[f][e]
					max_i = i
			alignments[max_i].append(j+1)

		all_alignments.append(alignments)

	return all_alignments

def evaluate(alignments, n=1000):
	gold = list(open('corpus_1000_ennl_viterbi', 'r'))
	j = 0
	correct = 0.0
	total = 0.0
	r_total = 0.0
	for i in xrange(2, len(gold)+1):
		if j == n:
			break
		if i % 3 == 0:
			alignment = alignments[j]
			res = evaluate_alignment(alignment, gold[i-1])
			correct += res[0]
			total += res[1]
			r_total += res[2]
			j+=1
	print "precision: ", (correct / total)*100.0
	print "recall: ", (correct / r_total)*100.0

def evaluate_alignment(alignment, giza_gold):
	"""

	@param alignment:
	@param giza_gold:
	@return: (correct alignments, total alignments)
	"""
	correct = 0.0
	total = 0.0
	r_total = 0.0
	matches = re.findall('\({[ 0-9]*}\)', giza_gold)
	for m, match in enumerate(matches):
		gold_a = [int(x) for x in match[2:-2].strip().split()]
		r_total += len(gold_a)
		for a in alignment[m]:
			if a in gold_a:
				correct += 1.0
			total += 1.0

	return correct, total, r_total

def intersect_alignments(al1, al2):
	res= [[] for _ in xrange(len(al1))]
	for i, a1 in enumerate(al1):
		for j, a in enumerate(a1):
			if i in al2[a]:
				res[i].append(a)
	return res

def alignments_intersection(als1, als2):
	alignments = []
	for i in xrange(len(als1)):
		alignments.append(intersect_alignments(als1[i], als2[i]))
	return alignments

if __name__ == '__main__':
	# Example uses:
	# round_dc(translate(pairs))
	n = 1000
	iters = 20
	C = [a for a in corpus(n)]
	t = translate(C, iters)
	alignments1 = getViterbiAlignment(C, t)
	pickle.dump(alignments1, open('alignments1', 'wb'))
	evaluate(alignments1, n)
	C = [a for a in corpus(n, flip=True)]
	t = translate(C, iters)
	alignments2 = getViterbiAlignment(C, t)
	pickle.dump(alignments2, open('alignments2', 'wb'))
	alignments = alignments_intersection(alignments1, alignments2)
	evaluate(alignments, n)