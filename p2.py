import numpy as np
from pprint import pprint
from collections import Counter


def extract(A, f_sent, f_start, f_end, e_sent, e_start, e_end):
	# check if at least one alignment point
	if f_end == -1 or abs(f_end - f_start) > 4:
		return []

	# check if alignment points violate consistency
	# ----This part of the Koehn algorithm doesnt make any sense to me so I changed it
	e_match = [a[0] for a in A if f_start <= a[1] <= f_end]
	for e in e_match:
		if e < e_start or e > e_end:
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


def extract_phrase_pairs(n=10):
	ffile = open('project2_data/training/p2_training.en', 'r')
	efile = open('project2_data/training/p2_training.nl', 'r')
	alfile = open('project2_data/training/p2_training_symal.nlen', 'r')

	BP = {}

	i = 0
	while i < n:
		f_sent = ffile.readline().split()
		e_sent = efile.readline().split()
		al = [a.split('-') for a in alfile.readline().split()]
		A = [(int(a[0]), int(a[1])) for a in al]

		for e_start in xrange(0, len(e_sent)):
			e_range = e_start + 4
			erange = e_range if e_range < len(e_sent) else len(e_sent)
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


BP = extract_phrase_pairs()
# pprint([(key, counter) for key, counter in BP.iteritems() if sum(counter.values()) > 100])
pprint(BP)