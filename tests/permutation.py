from unittest import TestCase
from collections import Counter
from p2 import find_concatenated_phrase

__author__ = 'louissmit'


class permutation(TestCase):
	def setUp(self):
		self.phrasetable = {'.': Counter({'.': 1.0}),
							'er': Counter({'there': 1.0}),
							'gebrek': Counter({'lack': 1.0}),
							'gebrek aan': Counter({'lack of': 1.0}),
							'gebrek aan transparantie': Counter(
								{'lack of transparency': 0.5, 'lack of transparency .': 0.5}),
							'het': Counter({'the': 1.0}),
							'het gebrek': Counter({'the lack': 1.0}),
							'het gebrek aan': Counter({'the lack of': 1.0}),
							'is': Counter({'is': 0.5, 'there': 0.5}),
							'is er': Counter({'there': 1.0}),
							'is er nog': Counter({'there is': 1.0}),
							'nog': Counter({'the': 1.0}),
							'nog het gebrek': Counter({'the lack': 1.0}),
							'tot': Counter({'finally': 1.0}),
							'tot slot is': Counter({'finally , there': 1.0}),
							'transparantie': Counter(
								{'transparency': 0.6666666666666666, 'transparency .': 0.3333333333333333}),
							'transparantie .': Counter({'transparency .': 0.5, 'transparency': 0.5})}
		self.phrasepair = ('het gebrek aan transparantie', 'the lack of transparency')

	def test_find_concatenated_phrase(self):
		find_concatenated_phrase(self.phrasepair, self.phrasetable)

