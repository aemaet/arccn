import csv,pickle,os

dirs = ['zoo_net','merlin_net','rf_net']
res = []
for d in dirs:
	files = os.listdir(d)
	for f in files:
		pf = open(d + '/' + f,'rb')
		n = pickle.load(pf)
		tmp = { 'name': n.meta,
				'n_nodes': n.topology.number_of_nodes(),
				'n_edges': n.topology.number_of_edges()}
		res.append(tmp)
		pf.close()

with open('table.csv', 'w') as csvfile:
	fieldnames = ['name', 'n_nodes', 'n_edges']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()
	for r in res:
		writer.writerow(r)