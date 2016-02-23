import random, copy

def loadWithRandomSamples(database):
	growDB = []

	temp_db = copy.copy(database)

	total = int(2 * len(database) / 3)
	for i in range(0, total):
		elem = random.choice(temp_db)
		growDB.append(elem)
		temp_db.remove(elem)

	pruneDB = temp_db

	return growDB, pruneDB

def loadWithRandomSamplesByClass(database, classList):
	growDB = []

	temp_db = copy.copy(database)

	class_data = {}
	for c in classList:
		class_data[c] = {}
		class_data[c]['size'] = 0
		class_data[c]['elements'] = []

	for d in temp_db:
		if d.classification[0] in class_data:
			class_data[d.classification[0]]['elements'].append(d)
			class_data[d.classification[0]]['size'] = class_data[d.classification[0]]['size'] + 1

	for key in class_data:
		total = int(2 * class_data[key]['size'] / 3)

		for i in range(0, total):
			elem = random.choice(class_data[key]['elements'])
			growDB.append(elem)
			class_data[key]['elements'].remove(elem)
			temp_db.remove(elem)

	pruneDB = temp_db

	return growDB, pruneDB
