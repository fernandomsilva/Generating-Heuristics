import pickle

class DBEntry:
	def __init__(self, player_cards, dealer_card):
		self.player_cards = player_cards
		self.dealer_card = dealer_card
		self.classification = ("", 0.0)
		self.rank = {}

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
