from Pblackjack import *

import pandas as pd

'''
249
if points >= 9 and points <= 11 and dealer_points <= 7 then double_down
315
if points >= 10 and points <= 11 and dealer_points <= 9 then double_down
331
if points >= 13 and dealer_points <= 6 then stand
439
if points >= 17 then stand
480
if points >= 9 and dealer_points >= 5 and dealer_points <= 6 then stand
490
if points <= 4 and dealer_points <= 3 then stand
492
'''
def selectMove(points, dealer_points, depth):
	if points >= 9 and points <= 11 and dealer_points <= 7 and depth >= 1:
		return 'double_down'
	if points >= 10 and points <= 11 and dealer_points <= 9 and depth >= 2:
		return 'double_down'
	if points >= 13 and dealer_points <= 6 and depth >= 3:
		return 'stand'
	if points >= 17 and depth >= 4:
		return 'stand'
	if points >= 9 and dealer_points >= 5 and dealer_points <= 6 and depth >= 5:
		return 'stand'
	if points <= 4 and dealer_points <= 3 and depth >= 6:
		return 'stand'

	return 'hit'

def evaluateGame(depth=0, n=10000):
	evaluator = GameEvaluator(deck=make_deck(8))
	return evaluator.Experiment(depth, n)

class GameEvaluator:
	def __init__(self, deck=make_deck(8)):
		self.deck = copy.copy(deck)

	def Play(self, depth):
		game = GameNode(deck=self.deck)

		game.setup()
		
		while len(game.possible_moves()) > 0:
			move = selectMove(max([0] + [y for y in game.points if y < 22]), max([0] + [y for y in game.dealer_points if y < 22]), depth)
			game = game.push_move(move)

		game.dealerPlays()

		return game.win()

	def Experiment(self, depth, n=10000):
		data = pd.Series([self.Play(depth) for i in xrange(n)])

		return float(data.sum()) / len(data)

for i in range(0, 7):
	print evaluateGame(i, 2000000)