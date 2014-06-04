from B import B
import numpy as np
from training import train
from sent_utils import get_alignments, get_german_prime
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


def iterate_local_search(corpus):
	converged = False
	while not converged:
		last_score = new_score
		for i, sent in enumerate(corpus):
			delta, bp = localSearch(b, sent)
			corpus[i] = traverseBackpointers(sent, delta, bp, 0, len(sent))

		new_score = calculate_score(corpus)
		converged = (last_score - new_score) < 0.1
	return corpus

def calculate_score(corpus):
	return 22.4


if __name__ == '__main__':
	# testing oracle reordering
	set = 'training'
	english = open('../project2_data/'+set+'/p2_'+set+'.en', 'r').readline().split()
	german = list(open('../project2_data/'+set+'/p2_'+set+'.nl', 'r'))[22].split()

	alignment = get_alignments()[0]

	print german
	print get_german_prime(german, alignment)
	# print english

	# testing local search
	# sent = 'beta alpha gamma zeta crap'.split()
	sent = german
	# b = B().initAlphabetically(sent)
	# clf, word_vecs = train(n=100)
	# pickle.dump((clf, word_vecs), open( "model.p", "wb" ) )
	clf, word_vecs = pickle.load(open( "model.p", "rb" ))

	b = B(clf, word_vecs)
	for i in xrange(0, 10):
		delta, bp = localSearch(b, sent)
		sent = traverseBackpointers(sent, delta, bp, 0, len(sent))
		print sent
