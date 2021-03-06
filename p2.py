import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from collections import Counter
import itertools

def extract(A, f_sent, f_start, f_end, e_sent, e_start, e_end):
	"""
	Given a phrase pair, returns the set of consistent phrase pairs associated with it.

	@param A: set of alignment tuples (f_a, e_a)
	@param f_sent: f sentence
	@param f_start: start index of f phrase to be considered
	@param f_end: endindex of f phrase to be considered
	@param e_sent: e sentence
	@param e_start: start index of e phrase to be considered
	@param e_end: end index of e phrase to be considered
	@return E: set of valid phrase pairs
	"""
	# check if at least one alignment point
	if f_end == -1 or abs(f_end - f_start) > 4:
		return []

	# check if alignment points violate consistency
	# ----This part of the Koehn algorithm doesnt make any sense to me so I changed it
	# 		check only for alignments that are within the f-side's borders
	for e, f in A:
		if (e < e_start or e > e_end) and (f_start <= f <= f_end):
			return []

	# add phrase pairs (incl. additional unaligned f)
	E = []
	f_s = f_start
	fa = [a[1] for a in A]
	while True:
		f_e = f_end
		while True:
			if e_start == e_end:
				e_phrase = e_sent[e_start]
			else:
				e_phrase = " ".join(e_sent[e_start:e_end])
			if f_s == f_e:
				f_phrase = f_sent[f_s]
			else:
				f_phrase = " ".join(f_sent[f_s:f_e])

			E.append((e_phrase, f_phrase))
			f_e += 1
			if f_e in fa or f_e > len(f_sent)\
				or abs(f_e - f_s) > 4:
				break
		f_s -= 1
		if f_s in fa or f_s < 0\
			or abs(f_e - f_s) > 4:
			break

	return E


def extract_phrase_table(n=1000, set='training'):
	"""
	Extracts a phrase table from a corpus of size n.

	@param n: amount of sentences to use
	@param set: which set: {'training', 'heldout', 'test'}
	@return: phrase table BP
	"""
	ffile = open('project2_data/'+set+'/p2_'+set+'.en', 'r')
	efile = open('project2_data/'+set+'/p2_'+set+'.nl', 'r')
	alfile = open('project2_data/'+set+'/p2_'+set+'_symal.nlen', 'r')

	BP = {}

	i = 0
	while i < n:
		f_sent = ffile.readline().split()
		e_sent = efile.readline().split()
		al = [a.split('-') for a in alfile.readline().split()]
		A = [(int(a[0]), int(a[1])) for a in al]

		for e_start in xrange(0, len(e_sent)):
			e_range = e_start + 4
			e_range = e_range if e_range < len(e_sent) else len(e_sent)
			for e_end in xrange(e_start, e_range):
				# find the minimally matching foreign phrase
				f_start, f_end = (len(f_sent), -1)
				for (e, f) in A:
					if e_start <= e <= e_end:
						f_start = min(f, f_start)
						f_end = max(f, f_end)

				# count phrase pairs
				for (e_phrase, f_phrase) in extract(A, f_sent, f_start, f_end, e_sent, e_start, e_end):
					if not BP.has_key(e_phrase):
						BP[e_phrase] = Counter()
					BP[e_phrase][f_phrase] += 1
		i += 1

	# conditional probabilities
	for e_phrase, counter in BP.iteritems():
		total = sum(counter.values())*1.0
		for f_phrase in counter:
			BP[e_phrase][f_phrase] /= total
	return BP


def calculate_coverage(heldout_phrasetable, train_phrasetable, candidate_range):
	"""
	Calculates coverage.

	@param heldout_phrasetable:
	@param train_phrasetable:
	@param candidate_range: nr of n-best f-phrases used
	@return: coverage
	"""
	total = 0.0
	right = 0.0
	concatright = 0.0
	for e_phrase, counter in heldout_phrasetable.iteritems():
		for f_phrase in counter:
			total += 1
			phrasepair = (e_phrase, f_phrase)
			if e_phrase in train_phrasetable:
				if f_phrase in train_phrasetable[e_phrase]:
					right += 1
					concatright += 1
			elif find_concatenated_phrase(phrasepair, train_phrasetable, candidate_range):
				concatright += 1

	print 'candidate_range: ', candidate_range
	print 'with concat: ', (concatright / total) * 100.0
	print 'without concat: ', (right / total) * 100.0
	return (concatright / total) * 100.0


def find_concatenated_phrase(phrasepair, phrasetable, candidate_range):
	"""
	Checks if a concatenation of up to 3 phrases is possible to achieve the phrasepair.

	@param phrasepair: to be realized
	@param phrasetable: phrase table
	@param candidate_range: nr of n-best f-phrases used
	@return: True if it can be built from concatenated phrase pairs, False otherwise
	"""
	e_phrase = phrasepair[0].split()
	f_phrase = phrasepair[1]
	for i1 in xrange(1,len(e_phrase)-1):
		for i2 in xrange(i1, len(e_phrase)):
			phrase1 = " ".join(e_phrase[:i1])
			phrase2 = " ".join(e_phrase[i1:i2])
			phrase3 = " ".join(e_phrase[i2:])
			phrases = [phrase1, phrase2, phrase3]

			# check 2 phrase inversion
			if i1 == i2 and (" ".join([phrase3, phrase1]) == f_phrase):
				return True
			# check if present in phrasetable
			nope = False
			for phrase in phrases:
				if phrase not in phrasetable:
					nope = True
					break
			# check all permutations of the candidate_range-most probable f-phrases
			if not nope:
				f_phrases = [phrasetable[phrase] for phrase in phrases]
				for indices in itertools.permutations([0, 1, 2]):
					candidate_f = [f_phrases[i].keys() for i in indices]
					for one in candidate_f[0][:candidate_range]:
						for two in candidate_f[1][:candidate_range]:
							for three in candidate_f[2][:candidate_range]:
								if " ".join([one, two, three]) == f_phrase:
									return True

	return False



if __name__ == '__main__':
	n = 100
	BP = extract_phrase_table(n=n)
	BP2 = extract_phrase_table(n=n, set='heldout')
	pres = []
	f = open('results'+str(n), 'w')
	for candidate_range in xrange(1, 100):
		pres.append(calculate_coverage(BP2, BP, candidate_range))
		print pres
		f.write(str(pres))

