import numpy as np
import re
from collections import Counter
from decimal import Context, Decimal
# pairs = [(a.split(), b.split()) for (a,b) in [('the dog','de hond'),('the cat','de kat'),('a dog','een hond'),('a cat','een kat')]]

def loadCorpus():
	source = list(open('corpus_1000.nl', 'r'))
	target = list(open('corpus_1000.en', 'r'))
	return source, target


def corpus(n=None):
	""" An iterator of pairs """
	source, target = loadCorpus()
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

def translate(pairs, n=20, stability=1):
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
	i = 0
	while i < n:
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

		log_pp = 0
		for (fs, es) in pairs:
			p = 0.0
			for f in fs:
				for e in es:
					p += t[f][e]
			p *= (epsilon/(len(fs)**len(es)))
			log_pp += np.log2(p)
		old_perplexity = Decimal(perplexity)
		# perplexity = Context().power(2, Decimal(-log_pp))#2**(-perplexity)
		# stable = abs(old_perplexity - perplexity) < stability
		print 'perplexity:', log_pp, ('stable' if stable else 'not stable')
		i += 1

	return t


def getViterbiAlignment(pairs, t):
	"""
	Gets viterbi alignment
	@param source:
	@param target:
	@param t: Translation model
	"""
	all_alignments = []
	for (f_s, e_s) in pairs:
		alignments = [[] for _ in xrange(len(e_s))]
		for j, f in enumerate(f_s):
			max = -1
			max_i = -1
			for i, e in enumerate(e_s):
				# print "t("+e+"|f) ", t[f][e]
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
	for i in xrange(2, len(gold)+1):
		if j == n:
			break
		if i % 3 == 0:
			print gold[i-2]
			alignment = alignments[j]
			res = evaluate_alignment(alignment, gold[i-1])
			correct += res[0]
			total += res[1]
			j+=1
	print (correct / total)*100.0

def evaluate_alignment(alignment, gold):
	"""

	@param alignment:
	@param gold:
	@return:
	"""
	correct = 0.0
	total = 0.0
	matches = re.findall('\({[ 0-9]*}\)', gold)
	for a, match in enumerate(matches):
		for gold_a in match[2:-2].strip().split():
			if int(gold_a) in alignment[a]:
				correct += 1.0
			total += 1.0
	return correct, total


if __name__ == '__main__':
	# Example uses:
	# round_dc(translate(pairs))
	n = 1000
	C = [a for a in corpus(n)]
	t = translate(C, 20)
	alignments = getViterbiAlignment(C, t)
	evaluate(alignments, n)