def slice_l(step,l):
	res = [[] for x in range(step)]
	for i in range(step):
		for j in range(i,len(l),step):
			print j
			res[i].append(l[j])
		print res
	return res
a = range(9)
b = range(18)
print slice_l(2,b)