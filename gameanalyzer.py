from Pblackjack import *
from loadtable import *

import pandas as pd

class GameTrace:
	def __init__(self, pCards, dCards, pPoints, dPoints, r):
		self.player_cards = pCards
		self.dealer_cards = dCards
		self.player_points = pPoints
		self.dealer_points = dPoints
		self.result = r

	def __str__(self):
		return "Player: Cards " + str(self.player_cards) + " | Points: " + str(self.player_points) + " /\/\/\ Dealer: Cards " + str(self.dealer_cards) + " | Points: " + str(self.dealer_points) + " /\/\/\ Score: " + str(self.result)

def saveTraceData(filename, db):
	f = open(filename, 'wb')

	for x in db:
		pickle.dump(x, f)

	f.close()

def alternateSetup(game):
	#game.hand = [self.drawCard(), self.drawCard()]
	game.hand = [Card('10', [10], 'H'), Card('9', [9], 'H')]
	game.points = game.totalHandPoints(game.hand)

	game.dealer_hand = [Card('9', [9], 'C')]
	game.dealer_points = game.totalHandPoints(game.dealer_hand)
	
	game.split_hand = []
	game.split_points = 0
	game.split_done = False
	
	game.movein = []
	game.split_movein = []
	
	game.moves = game.possible_moves()

	return

def evaluateGame(move, db, n=200000):
	evaluator = GameEvaluator(deck=make_deck(8))
	return evaluator.Experiment(move, db, n)

class GameEvaluator:
	def __init__(self, deck=make_deck(8)):
		self.deck = copy.copy(deck)

	def Play(self, move, db):
		game = GameNode(deck=self.deck)

		alternateSetup(game)

		game = game.push_move(move)
		
		while len(game.possible_moves()) > 0:
			#print "pp: " + str(max([0] + [y for y in game.points if y < 22]))
			#print "dp: " + str(max([0] + [y for y in game.dealer_points if y < 22]))
			#print lookuptable
			#print lookuptable[max([0] + [y for y in game.points if y < 22])][max([0] + [y for y in game.dealer_points if y < 22])]
			game = game.push_move(lookuptable[max([0] + [y for y in game.points if y < 22])][max([0] + [y for y in game.dealer_points if y < 22])])
			currentPoints = max([0] + [y for y in game.points if y < 22])

		game.dealerPlays()

		db.append(GameTrace([x.name for x in game.hand], [y.name for y in game.dealer_hand], max([0] + [x for x in game.points if x < 22]), max([0] + [x for x in game.dealer_points if x < 22]), game.win()))

		return game.win()

	def Experiment(self, move, db, n=20):
		data = pd.Series([self.Play(move, db) for i in xrange(n)])

		return float(data.sum()) / len(data)

lookuptable = {}
for i in range(4, 22):
	lookuptable[i] = {}
	for j in range(2, 12):
		lookuptable[i][j] = None


def evalPoints(pc):
	points = 0

	for card in pc:
		if card == "A":
			points = points + 11
		else:
			points = points + int(card)

	return points


database = loadData('blackjacktable.dt')

print len(database)

for i in range(0, len(database)):
	if 'A' not in database[i].player_cards:
		if evalPoints(database[i].player_cards) in lookuptable:
			if lookuptable[evalPoints(database[i].player_cards)][evalPoints([database[i].dealer_card])] == None:
				lookuptable[evalPoints(database[i].player_cards)][evalPoints([database[i].dealer_card])] = database[i].classification[0]

tracedb = []

print evaluateGame('double_down', tracedb)

saveTraceData('traceDB.dt', tracedb)

for t in tracedb:
	print str(t)
