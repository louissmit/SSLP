from sklearn.linear_model import SGDClassifier
import os.path
from sent_utils import get_alignments, get_german_prime
import numpy as np
import cPickle as pickle
from pprint import pprint
import gensim

def features(model, sent, left, right, flip=False):
	def get(i):
		if i >= 0 and i < len(sent):
			return model[sent[i]]
		else:
			return np.zeros(model.layer1_size)

	sum = [np.sum([get(i) for i in [-1] + range(left + 1, right - 1)], axis=0)]
	if flip:
		left, right = right, left
	conc = [get(i) for i in [left - 1, left, left + 1]]
	conc += sum
	conc += [get(i) for i in [right - 1, right, right + 1]]
	return np.concatenate(conc)


def create_training_set(g_primes, word_vecs):
	X = []
	Y = []
	n = len(g_primes)
	filename = 'trainingset_n='+str(n)+'.npz'
	if not os.path.isfile(filename):
	# if True:
		print "Creating training set.."
		for g_prime in g_primes:
			for i in xrange(0, len(g_prime)):
				for j in xrange(i+1, len(g_prime)):
					true_vector = features(word_vecs, g_prime, i, j)
					X.append(true_vector)
					Y.append(1)
					false_vector = features(word_vecs, g_prime, i, j, flip=True)
					X.append(false_vector)
					Y.append(0)

		print "Serializing dataset.."
		# pickle.dump((X, Y), open(filename, "w"))
		np.savez(filename, X, Y)
	else:
		print "Loading training set.."
		# X, Y = pickle.load(open(filename, "r"))
		files = np.load(filename)
		X = files['arr_0']
		Y = files['arr_1']
	return X, Y

def train(word_vecs, g_primes, n):

	filename = 'model_n='+str(n)
	if not os.path.isfile(filename):
	# if True:
		print "Training classifier.."
		clf = SGDClassifier(loss="hinge", penalty="l2")
		for g_prime in g_primes:
			for i in xrange(0, len(g_prime)):
				for j in xrange(i+1, len(g_prime)):
					X = []
					Y = []
					true_vector = features(word_vecs, g_prime, i, j)
					X.append(true_vector)
					Y.append(1)
					false_vector = features(word_vecs, g_prime, i, j, flip=True)
					X.append(false_vector)
					Y.append(0)
					clf.partial_fit(X, Y, np.asarray([0, 1]))
		pickle.dump(clf, open(filename, "wb"))

	else:
		print "Loading classifier.."
		clf = pickle.load(open(filename, "rb" ))

	return clf


def test_classifier(clf, X, Y):
	print "Testing.."
	gut = 0
	all = 0
	for i, x in enumerate(X):
		y = Y[i]
		pred = clf.predict(x)
		if pred == y:
			gut+=1;
		all+=1;
	print (gut*1.0) / all




