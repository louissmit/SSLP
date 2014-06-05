from B import B
import numpy as np
from training import train
from sent_utils import get_alignments, get_german_prime, get_word_vecs
from bleu import bleu, precision

import cPickle as pickle

def localSearch(B, sent):
	"""
	Searches for the best local permutation

	@rtype : tuple
	@param B: word pair preference matrix
	@param sent: input sentence
	@return: (delta, backpointers)
	"""
	n = len(sent)
	beta = np.zeros((n+1,n+1))
	bp = np.zeros((n+1,n+1))
	delta = np.zeros((n+1,n+1,n+1))

	# for i in xrange(0, n):
	# 	beta[i, i+1] = 0
	# 	for k in xrange(i+1, n+1):
	# 		delta[i, i, k] = 0
	# 		delta[i, k, k] = 0

	for w in xrange(2, n+1):
		for i in xrange(0, n-w+1):
			k = i + w
			beta[i, k] = float("-inf")
			for j in xrange(i+1, k):
				delta[i, j, k] = delta[i, j, k-1] + delta[i+1, j, k] - delta[i+1, j, k-1] + B.get(sent, k-1, i) - B.get(sent, i, k-1)
				new_beta = beta[i, j] + beta[j, k] + max(0, delta[i, j, k])
				if new_beta > beta[i, k]:
					beta[i, k] = new_beta
					bp[i, k] = j
	# print beta
	return delta, bp


def traverseBackpointers(sent, delta, bp, i, k):
	"""
	Recursively finds the permutation from the backpointers provided by localSearch

	@param sent: input sentence
	@param delta: swap probabilities
	@param bp: backpointers
	@param i: first index of range
	@param k: last index of range
	@return: permutation of input sentence
	"""
	j = int(bp[i, k])
	if (k - i) > 1:
		if delta[i, j, k] > 0:
			return traverseBackpointers(sent, delta, bp, j, k) + traverseBackpointers(sent, delta, bp, i, j)
		else:
			return traverseBackpointers(sent, delta, bp, i, j) + traverseBackpointers(sent, delta, bp, j, k)
	else:
		return [sent[i]]


def iterate_local_search(b, corpus, g_prime, n=10):
	converged = False
	new_score = 0.0
	while not converged:
		last_score = new_score
		for i, sent in enumerate(corpus):
			if i == n: break
			print sent
			delta, bp = localSearch(b, sent)
			corpus[i] = traverseBackpointers(sent, delta, bp, 0, len(sent))

		new_score = calculate_score(corpus, g_prime, n)
		print new_score
		converged = (new_score - last_score) < 0.001
	return corpus

def calculate_score(corpus, g_prime, n=10):
	res = 0.0
	for i, sent in enumerate(corpus):
		if i == n: break
		res += bleu(g_prime[i], sent)
	return res / n


if __name__ == '__main__':
	# testing oracle reordering
	n = 1000
	set = 'training'
	english = open('../project2_data/'+set+'/p2_'+set+'.en', 'r').readline().split()
	german = [sent.split() for sent in list(open('../project2_data/'+set+'/p2_'+set+'.nl', 'r'))][:n]

	alignments = get_alignments(n=n)
	g_prime = [get_german_prime(sent, alignments[i]) for i, sent in enumerate(german)]

	# testing local search
	# sent = 'beta alpha gamma zeta crap'.split()
	# sent = german[1]
	# print sent
	# g_sent = g_prime[1]
	# print g_sent
	# print precision(g_sent, sent)
	# b = B().initAlphabetically(sent)
	word_vecs = get_word_vecs(german, n=n)
	clf = train(word_vecs, n=n)


	# b = B(clf, word_vecs)
	# iterate_local_search(b, german, g_prime, n=1)

# 1000 = 15.3
