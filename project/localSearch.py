from B import B
import numpy as np

def localSearch(B, sent):
	"""
	@todo backpointers

	@param B:
	@param sent:
	@return:
	"""
	n = len(sent)
	beta = np.zeros((n+1,n+1))
	delta = np.zeros((n+1,n+1,n+1))
	for i in xrange(0, n):
		beta[i, i+1] = 0
		for k in xrange(i+1, n+1):
			delta[i, i, k] = 0
			delta[i, k, k] = 0

	for w in xrange(2, n+1):
		for i in xrange(0, n-w):
			k = i + w
			beta[i, k] = float("-inf")
			best_i = "not_assigned"
			best_j = "not_assigned"
			best_k = "not_assigned"
			for j in xrange(i+1, k):
				delta[i, j, k] = delta[i, j, k-1] + delta[i+1, j, k] - delta[i+1, j, k-1] + B.get(sent[k], sent[i+1]) - B.get(sent[i+1], sent[k])
				new_beta = beta[i, j] + beta[j, k] + max(0, delta[i, j, k])
				if new_beta > beta[i, k]:
					beta[i, k] = new_beta
					best_i = i
					best_j = j
					best_k = k
			print best_i, best_j, best_k

	print beta
	return beta[0, n]


if __name__ == '__main__':
	b = B()
	print localSearch(b, 'I am just testing'.split())
