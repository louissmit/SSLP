from B import B
import numpy as np
from training import train, test_classifier, create_training_set
from sent_utils import get_alignments, get_german_prime, get_word_vecs, save
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
	beta = np.zeros((n + 1, n + 1))
	bp = np.zeros((n + 1, n + 1))
	delta = np.zeros((n + 1, n + 1, n + 1))

	# for i in xrange(0, n):
	# 	beta[i, i+1] = 0
	# 	for k in xrange(i+1, n+1):
	# 		delta[i, i, k] = 0
	# 		delta[i, k, k] = 0

	for w in xrange(2, n + 1):
		for i in xrange(0, n - w + 1):
			k = i + w
			beta[i, k] = float("-inf")
			for j in xrange(i + 1, k):
				delta[i, j, k] = delta[i, j, k - 1] + delta[i + 1, j, k] - delta[i + 1, j, k - 1] + B.get(sent, k - 1,
																										  i) - B.get(
					sent, i, k - 1)
				new_beta = beta[i, j] + beta[j, k] + max(0, delta[i, j, k])
				if new_beta > beta[i, k]:
					beta[i, k] = new_beta
					bp[i, k] = j
	print beta.max()
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


def iterate_local_search(b, test_corpus, g_prime):
	converged = False
	new_score = 0.0
	not_improved = 0.0
	while not_improved < 2:
		last_score = new_score
		for i, sent in enumerate(test_corpus):
			# print 'input:', sent
			delta, bp = localSearch(b, sent)
			test_corpus[i] = traverseBackpointers(sent, delta, bp, 0, len(sent))
			# print 'result:', test_corpus[i]

		new_score = calculate_score(test_corpus, g_prime)
		print new_score
		if (new_score - last_score) > 0:
			not_improved = 0
		else:
			not_improved += 1
	return test_corpus


def calculate_score(test_corpus, g_prime):
	res = 0.0
	for i, sent in enumerate(test_corpus):
		res += bleu(g_prime[i], sent)
	return res / train_set_size


if __name__ == '__main__':
	# testing oracle reordering
	train_set_size = 10000
	test_set_size = 100
	set = 'training'
	english = [sent.split() for sent in list(open('../project2_data/' + set + '/p2_' + set + '.en', 'r'))][
			  :train_set_size]
	german = [sent.split() for sent in list(open('../project2_data/' + set + '/p2_' + set + '.nl', 'r'))]
	# word_vecs = get_word_vecs(german)
	german_test = german[train_set_size:train_set_size + test_set_size]
	german = german[:train_set_size]
	alfile = [al.split() for al in list(open('../project2_data/' + set + '/p2_' + set + '_symal.nlen', 'r'))][
			 :train_set_size]

	aligns = get_alignments(alfile)
	g_prime = [get_german_prime(sent, aligns[i]) for i, sent in enumerate(german)]
	name = 'gprimes_n='+str(train_set_size)
	save(g_prime, name)

	# clf = train(word_vecs, g_prime, train_set_size)
	# # print len(X)
	# g_prime_test = [get_german_prime(sent, aligns[i]) for i, sent in enumerate(german_test)]
	# X, Y = create_training_set(g_prime_test, word_vecs)
	# test_classifier(clf, X, Y)
	# print clf.score(X, Y)
	#
	# b = B(clf, word_vecs)
	# test_corpus_indices = [i for i, sent in enumerate(german) if len(sent) < 20][:test_set_size]
	# test_corpus = [german[i] for i in test_corpus_indices]
	# test_corpus_en = [english[i] for i in test_corpus_indices]
	# test_corpus_als = [alfile[i] for i in test_corpus_indices]
	# alignments = get_alignments(test_corpus_als)
	# g_prime = [get_german_prime(sent, alignments[i]) for i, sent in enumerate(test_corpus)]
	#
	# # for sent_i in xrange(0, test_set_size):
	# # 	sent = test_corpus[sent_i]
	# # 	print sent
	# # 	print test_corpus_en[sent_i]
	# # 	prime_sent = g_prime[sent_i]
	# # 	print prime_sent
	# # 	b = b.initAlphabetically(sent, prime_sent)
	# # 	delta, bp = localSearch(b, sent)
	# # 	print traverseBackpointers(sent, delta, bp, 0, len(sent))
	# # print b.correct * 1.0 / b.total
	#
	# iterate_local_search(b, test_corpus, g_prime)

