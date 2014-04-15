from unittest import TestCase
from p1 import evaluate_alignment
from p1 import intersect_alignments
import numpy as np

__author__ = 'louissmit'


class evaluation(TestCase):
	def setUp(self):
		self.gold = "NULL ({ }) this ({ }) is ({ }) what ({ 1 }) we ({ }) need ({ 2 }) for ({ 3 }) ships ({ 4 5 6 7 }) . ({ 8 }) "
		self.perfect_alignment = [[], [], [], [1], [], [2], [3], [4, 5, 6, 7], [8]]

	def test_evaluate_alignment(self):
		right, total = evaluate_alignment(self.perfect_alignment, self.gold)
		self.assertEqual(right, total)

class alignmentIntersection(TestCase):

	def setUp(self):
		self.alignment1 = [[], [], [], [1], [], [2], [3], [4, 5, 6, 7], [8]]
		self.alignment2 = [[], [], [], [8], [7], [], [1, 2, 3, 4, 5, 6], [], []]

	def test_intersection(self):
		intersect_alignments(self.alignment1, self.alignment2)
