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

def get_german_prime(german_sent, alignments):
	"""
	Reordering oracle, Tromble & Eisner refer to it as german'

	@param german_sent: german input sentence
	@param alignments: dictionary with alignments to english e.g. {0: [1, 2], 1: [4,1]}
	@return: german'
	"""
	indices = []
	for g, g_word in enumerate(german_sent):
		if g in alignments:
			indices.append(min(alignments[g]))
		else:
			indices.append(0)
	indices = np.argsort(np.array(indices), kind='mergesort')
	g_prime = [german_sent[i] for i in indices]
	return g_prime


if __name__ == '__main__':
	# testing oracle reordering
	set = 'training'
	english = open('../project2_data/'+set+'/p2_'+set+'.en', 'r').readline().split()
	german = open('../project2_data/'+set+'/p2_'+set+'.nl', 'r').readline().split()
	alfile = [a.split('-') for a in open('../project2_data/'+set+'/p2_'+set+'_symal.nlen', 'r').readline().split()]
	alignments = {}
	for a in alfile:
		g_al = int(a[0])
		if g_al not in alignments:
			alignments[int(a[0])] = []
		alignments[int(a[0])].append(int(a[1]))

	print german
	print get_german_prime(german, alignments)
	print english

	# testing local search
	sent = 'beta alpha gamma zeta crap'.split()
	b = B().initAlphabetically(sent)
	delta, bp = localSearch(b, sent)
	print traverseBackpointers(sent, delta, bp, 0, len(sent))
