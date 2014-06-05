import numpy as np
from pprint import pprint
from sent_utils import get_german_prime
from training import features

class B:
	def __init__(self, clf, word_vecs):
		self.matrix = {}
		self.clf = clf
		self.word_vecs = word_vecs

	def get(self, sent, left_word, right_word):
		# return np.random.random_sample()
		# return self.matrix[sent[left_word]][sent[right_word]]
		res = self.clf.predict(features(self.word_vecs, sent, left_word, right_word))
		return res


	def initAlphabetically(self, sent, g_prime):
		# alphabetic preference matrix for testing purposes
		# sorted_sent = []
		# for x in sorted(sent):
		# 	sorted_sent.append(x)
		sorted_sent = g_prime
		print sorted_sent
		for i, left_word in enumerate(sorted_sent):
			if left_word not in self.matrix:
				self.matrix[left_word] = {}
			for j in xrange(i, len(sent)):
				right_word = sorted_sent[j]
				if right_word not in self.matrix:
					self.matrix[right_word] = {}
				if right_word not in self.matrix[left_word]:
					self.matrix[left_word][right_word] = 1
				if left_word not in self.matrix[right_word]:
					self.matrix[right_word][left_word] = 0

		return self


