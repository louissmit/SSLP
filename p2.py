import numpy as np

f_sent = open('project2_data/training/p2_training.en', 'r').readline().split()
e_sent = open('project2_data/training/p2_training.nl', 'r').readline().split()
al = open('project2_data/training/p2_training_symal.nlen', 'r').readline().split()

al = [a.split('-') for a in al]
A = [(int(a[0]), int(a[1])) for a in al]
print A
print len(f_sent)



def extract(A, f_sent, f_start, f_end, e_sent, e_start, e_end):
	if f_end == 0:
		return []

	for (e, f) in A:
		# print 'yes', e_start, e, e_end
		if e < e_start or e > e_end:
			# print 'no', e_start, e, e_end
			return []

	E = []
	f_s = f_start
	print f_start, f_end
	while f_s > 0:
		f_e = f_end
		while f_e < len(f_sent):
			E.append((e_sent[e_start:e_end], f_sent[f_start:f_end]))
			print E
			f_e += 1
		f_s -= 1

	return E


BP = []
for e_start in xrange(0, len(e_sent)):
	for e_end in xrange(e_start, len(e_sent)):
		f_start, f_end = (len(f_sent), 0)
		for (e, f) in A:
			if e_start <= e <= e_end:
				f_start = min(f, f_start)
				f_end = max(f, f_end)

			BP += extract(A, f_sent, f_start, f_end, e_sent, e_start, e_end)