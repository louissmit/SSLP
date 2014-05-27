import numpy as np
from pprint import pprint


class B:
	def __init__(self, sent):
		# alphabetic preference matrix for testing purposes
		sorted_sent = []
		for x in sorted(sent):
			sorted_sent.append(x)
		print sorted_sent
		self.matrix = {}
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

		# pprint(self.matrix)


	def get(self, left_word, right_word):
		# return np.random.random_sample()
		return self.matrix[left_word][right_word]
