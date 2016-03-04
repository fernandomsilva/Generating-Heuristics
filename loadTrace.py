import pickle

class GameTrace:
	def __init__(self, pCards, dCards, pPoints, dPoints, r):
		self.player_cards = pCards
		self.dealer_cards = dCards
		self.player_points = pPoints
		self.dealer_points = dPoints
		self.result = r

	def __str__(self):
		return "Player: Cards " + str(self.player_cards) + " | Points: " + str(self.player_points) + " /\/\/\ Dealer: Cards " + str(self.dealer_cards) + " | Points: " + str(self.dealer_points) + " /\/\/\ Score: " + str(self.result)

def loadData(filename):
	#f = open('fulldatatable.csv', 'rb')
	f = open(filename, 'rb')

	database = []

	#for element in f:
	try:
		while True:
			database.append(pickle.load(f))
	except:
		pass

	f.close()

	return database

d = loadData('traceDB.dt')

for t in d:
	print str(t)