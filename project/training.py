from sklearn.linear_model import SGDClassifier
import os.path
from sent_utils import get_alignments, get_german_prime
import numpy as np
import cPickle as pickle
from pprint import pprint
import gensim

def features(model, sent, left, right):
	def get(i):
		if i >= 0 and i < len(sent):
			return model[sent[i]]
		else:
			return np.zeros(model.layer1_size)

	conc = [get(i) for i in [left - 1, left, left + 1]]
	conc += [np.sum([get(i) for i in [-1] + range(left + 1, right - 1)], axis=0)]
	conc += [get(i) for i in [right - 1, right, right + 1]]
	return np.concatenate(conc)


def create_training_set(g_primes, word_vecs):
	X = []
	Y = []
	n = len(g_primes)
	filename = 'trainingset_n='+str(n)
	if not os.path.isfile(filename):
	# if True:
		print "Creating training set.."
		for g_prime in g_primes:
			for i in xrange(0, len(g_prime)):
				for j in xrange(i+1, len(g_prime)):
					true_vector = features(word_vecs, g_prime, i, j)
					X.append(true_vector)
					Y.append(1)
					false_vector = features(word_vecs, g_prime, j, i)
					X.append(false_vector)
					Y.append(0)

		pickle.dump((X, Y), open(filename, "wb"))
	else:
		print "Loading training set.."
		X, Y = pickle.load(open(filename, "rb"))
	print 'asdfasdf'
	return X, Y

def train(X, Y, n):

	filename = 'model_n='+str(n)
	if not os.path.isfile(filename):
	# if True:
		print "Training classifier.."
		clf = SGDClassifier(loss="hinge", penalty="l2")
		clf.fit(X, Y)
		pickle.dump(clf, open(filename, "wb"))

	else:
		print "Loading classifier.."
		clf = pickle.load(open(filename, "rb" ))

	return clf


def test_classifier(clf, test_set):
	print "Testing.."
	gut = 0
	all = 0
	for test_sent in test_set:
		pred = clf.predict(test_sent)
		if pred == 1:
			gut+=1;
		all+=1;
		pred = clf.predict(test_sent)
		if pred == 0:
			gut+=1;
		all+=1;
	print (gut*1.0) / all




