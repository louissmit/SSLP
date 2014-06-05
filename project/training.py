from sklearn.linear_model import SGDClassifier
import os.path
from sent_utils import get_alignments, get_german_prime
import numpy as np
import cPickle as pickle
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


def create_training_set(sents, aligns, word_vecs):
	X = []
	Y = []
	for w, sent in enumerate(sents):
		for i in xrange(0, len(sent)):
			for j in xrange(i, len(sent)):
				X.append(features(word_vecs, get_german_prime(sent, aligns[w]), i, j))
				Y.append(1)
				X.append(features(word_vecs, sent, j, i))
				Y.append(0)
	return X, Y

def train(word_vecs, n=100):
	filename = 'model_n='+str(n)
	if not os.path.isfile(filename):
		set = 'training'
		german = list(open('../project2_data/'+set+'/p2_'+set+'.nl', 'r'))[:n]
		aligns = get_alignments(n=n)

		corpus = [s.split() for s in german]

		clf = SGDClassifier(loss="hinge", penalty="l2")
		X, y = create_training_set(corpus, aligns, word_vecs)
		clf.fit(X, y)
		pickle.dump(clf, open(filename, "wb"))

		gut = 0
		all = 0
		for x in xrange(0, 100):
			test = get_german_prime(corpus[x], aligns[x])
			for i in xrange(0, len(test)):
				for j in xrange(i, len(test)):
					pred = clf.predict(features(word_vecs, test, i, j))
					if pred == 1:
						gut+=1;
					all+=1;
					pred = clf.predict(features(word_vecs, test, j, i))
					if pred == 0:
						gut+=1;
					all+=1;


		print (gut*1.0) / all
	else:
		clf = pickle.load(open(filename, "rb" ))

	return clf

if __name__ == '__main__':
	train(n=20)


