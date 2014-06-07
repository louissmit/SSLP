import numpy as np
import gensim
import os.path
import cPickle as pickle
import json

def get_german_prime(german_sent, alignments):
	"""
	Reordering oracle, Tromble & Eisner refer to it as german'

	@param german_sent: german input sentence
	@param alignments: dictionary with alignments to english e.g. {0: [1, 2], 1: [4,1]}
	@return: german'
	"""
	indices = []
	for g, g_word in enumerate(german_sent):
		if g in alignments:
			indices.append(min(alignments[g]))
		else:
			indices.append(0)
	indices = np.argsort(np.array(indices), kind='mergesort')
	g_prime = [german_sent[i] for i in indices]
	return g_prime


def get_alignments(raw_aligns):
	alignments = []
	for i, als in enumerate(raw_aligns):
		al = [a.split('-') for a in als]
		alignment = {}
		for a in al:
			g_al = int(a[0])
			if g_al not in alignment:
				alignment[int(a[0])] = []
			alignment[int(a[0])].append(int(a[1]))
		alignments.append(alignment)
	return alignments

def get_word_vecs(corpus):
	n = len(corpus)
	file = 'word_vecs_n='+str(n)
	if os.path.isfile(file):
		print "Loading word vectors.."
		word_vecs = pickle.load(open(file, "rb" ))
	else:
		print "Training word vectors.."
		word_vecs = gensim.models.word2vec.Word2Vec(size=300, min_count=1, sg=0)
		word_vecs.build_vocab(corpus*2)
		word_vecs.train(corpus*2)
		pickle.dump(word_vecs, open(file, "wb" ) )
	return word_vecs

def reserialize_wordvecs(n=1000):
	file = 'word_vecs_n='+str(n)
	if os.path.isfile(file):
		print "Loading word vectors.."
		word_vecs = pickle.load(open(file, "rb" ))
		word_vecs.save_word2vec_format('word_vecs_n='+str(n) + '.txt', binary=False)

if __name__ == '__main__':
	reserialize_wordvecs()