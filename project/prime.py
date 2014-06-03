from localSearch import get_german_prime

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("e", help="home language corpus")
parser.add_argument("f", help="foreign language corpus")
parser.add_argument("a", help="alignment corpus")
args = parser.parse_args()

# oracle reordering

with open(args.e, 'r') as es, open(args.f, 'r') as fs, open(args.a, 'r') as als:
	for (e, f, al) in zip(es, fs, als):
		alfile = [a.split('-') for a in al.split()]
		alignments = {}
		for a in alfile:
			g_al = int(a[0])
			if g_al not in alignments:
				alignments[int(a[0])] = []
			alignments[int(a[0])].append(int(a[1]))

		print ' '.join(get_german_prime(f.split(), alignments))