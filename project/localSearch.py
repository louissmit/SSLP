

def localSearch(B, sent):
	"""
	@todo backpointers

	@param B:
	@param sent:
	@return:
	"""
	n = len(sent)
	beta = []
	delta = []
	for i in xrange(0, n-1):
		beta[i] = []
		beta[i][i+1] = 0
		for k in xrange(i+1, n):
			delta[i][i][k] = 0
			delta[i][k][k] = 0

	for w in xrange(2, n):
		for i in xrange(0, n-w):
			k = i + w
			beta[i][k] = -100000000
			for j in xrange(i+1, k-1):
				delta[i][j][k] = delta[i][j][k-1] + delta[i+1][j][k] - delta[i+1][j][k-1] + B.get(sent[k], sent[i+1]) - B.get(sent[i+1], sent[k])
				beta[i][k] = max(beta[i][k], beta[i][j] + beta[j][k] + max(0, delta[i][j][k]))

	return beta[0][n]
