from Pblackjack import *
import pandas as pd
import pickle, json

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
database = []

class DBEntry:
	def __init__(self, player_cards, dealer_card):
		self.player_cards = player_cards
		self.dealer_card = dealer_card
		self.classification = ("", 0.0)

temp = [DBEntry([x, y], z) for x in cards for y in cards for z in cards]
for e in temp:
	is_in = False
	for f in database:
		if e.player_cards[0] == f.player_cards[1] and e.player_cards[1] == f.player_cards[0] and e.dealer_card == f.dealer_card:
			is_in = True
			break
	if not is_in:
		database.append(e)

#for d in database:
#	print str(d.player_cards) + "    " + str(d.dealer_card) + "    " + str(database.index(d)) 

def setupGameWithEntry(game, dbEntry):
	game.split_hand = []
	game.split_points = 0
	game.split_done = False
	
	game.movein = []
	game.split_movein = []
	
	cards = [('2', [2]), ('3', [3]), ('4', [4]), ('5', [5]), ('6', [6]), ('7', [7]), ('8', [8]), ('9', [9]), ('10', [10]), ('J', [10]), ('Q', [10]), ('K', [10]), ('A', [1, 11])]
	temp_hand = []
	for entry in dbEntry.player_cards:
		for card in game.deck:
			if card.name == entry:
				temp_hand.append(card)
				game.deck.remove(card)
				break
	game.hand = temp_hand

	temp_dealer_hand = []
	for card in game.deck:
		if card.name == dbEntry.dealer_card:
			temp_dealer_hand.append(card)
			game.deck.remove(card)
			break
	game.dealer_hand = temp_dealer_hand

	game.points = game.totalHandPoints(game.hand)
	game.dealer_points = game.totalHandPoints(game.dealer_hand)

	game.moves = game.possible_moves()

def evaluateGame(move, dataEntry, n=10000):
	evaluator = GameEvaluator(deck=make_deck(8))
	return evaluator.Experiment(move, dataEntry, n)

class GameEvaluator:
	def __init__(self, deck=make_deck(8)):
		self.deck = copy.copy(deck)

	def Play(self, move, dataEntry):
		game = GameNode(deck=self.deck)

		setupGameWithEntry(game, dataEntry)

		#while len(game.possible_moves()) > 0:
		game = game.push_move(move)

		game.dealerPlays()

		return game.win()

	def Experiment(self, move, dataEntry, n=10000):
		data = pd.Series([self.Play(move, dataEntry) for i in xrange(n)])

		return float(data.sum()) / len(data)

f = open('table.csv', 'wb')
f2 = open('t.txt', 'w')

for i in range(0, len(database)):
	all_moves = ['stand', 'hit', 'double_down']
	best = (None, None)
	for m in all_moves:
		current = evaluateGame(m, database[i], 100000)
		if best[1] == None or best[1] < current:
			best = (m, current)

	database[i].classification = copy.copy(best)

	pickle.dump(database[i], f)
	json.dump(database[i].__dict__, f2)

	print i

f.close()
f2.close()