from B import B
import numpy as np

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

	for i in xrange(0, n):
		beta[i, i+1] = 0
		for k in xrange(i+1, n+1):
			delta[i, i, k] = 0
			delta[i, k, k] = 0

	for w in xrange(2, n+1):
		for i in xrange(0, n-w+1):
			k = i + w
			beta[i, k] = float("-inf")
			for j in xrange(i+1, k):
				delta[i, j, k] = delta[i, j, k-1] + delta[i+1, j, k] - delta[i+1, j, k-1] + B.get(sent[k-1], sent[i]) - B.get(sent[i], sent[k-1])
				new_beta = beta[i, j] + beta[j, k] + max(0, delta[i, j, k])
				if new_beta > beta[i, k]:
					beta[i, k] = new_beta
					bp[i, k] = j
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

if __name__ == '__main__':
	sent = 'beta alpha gamma zeta crap'.split()
	b = B(sent)
	delta, bp = localSearch(b, sent)
	print traverseBackpointers(sent, delta, bp, 0, len(sent))
