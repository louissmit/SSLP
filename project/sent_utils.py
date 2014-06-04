import numpy as np

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


def get_alignments(set='training', n=10):
	alfile = [al.split() for al in list(open('../project2_data/'+set+'/p2_'+set+'_symal.nlen', 'r'))]
	alignments = []
	for i, als in enumerate(alfile):
		if i == n: break
		al = [a.split('-') for a in als]
		alignment = {}
		for a in al:
			g_al = int(a[0])
			if g_al not in alignment:
				alignment[int(a[0])] = []
			alignment[int(a[0])].append(int(a[1]))
		alignments.append(alignment)
	return alignments