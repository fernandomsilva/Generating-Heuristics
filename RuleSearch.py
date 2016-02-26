from Pblackjack import *

import operator
import pickle
import pandas as pd

import multiprocessing

class RuleCondition:
	def __init__(self, parameter, operator, value):
		self.parameter = parameter
		self.operator = operator
		self.value = value

	def __str__(self):
		oper = "<=" if self.operator == operator.le else ">="
		return self.parameter + " " + oper + " " + str(self.value)


def loadRuleList(filename):
	f = open(filename, 'rb')

	rList = []

	#for element in f:
	try:
		while True:
			rList.append(pickle.load(f))
	except:
		pass

	f.close()

	return rList

def reference_dict(game):
	return {'points': max([0] + [x for x in game.points if x < 22]), 'dealer_points': max([0] + [x for x in game.dealer_points if x < 22])}

def evaluateWithRule(rule, reference_dict):
	condition_eval = False

	for condition in rule:
		if condition.operator(reference_dict[condition.parameter], condition.value):
			condition_eval = True
		else:
			condition_eval = False
			break

	if condition_eval:
		return True

	return False

def selectMove(rList, default_move, game):
	refDict = reference_dict(game)

	for (rule, move) in rList:
		if evaluateWithRule(rule, refDict):
			return move

	return default_move

def evaluateGame(rList, n=200000):
	evaluator = GameEvaluator(deck=make_deck(8))
	return evaluator.Experiment(rList, n)

class GameEvaluator:
	def __init__(self, deck=make_deck(8)):
		self.deck = copy.copy(deck)

	def Play(self, rList):
		game = GameNode(deck=copy.copy(self.deck))

		game.setup()
		
		while len(game.possible_moves()) > 0:
			move = selectMove(rList, default_class, game)
			#move = selectMove(game.hand, max([0] + [y for y in game.points if y < 22]), max([0] + [y for y in game.dealer_points if y < 22]), depth)

			game = game.push_move(move)

		game.dealerPlays()

		return game.win()

	def Experiment(self, rList, n=10000):
		data = pd.Series([self.Play(rList) for i in xrange(n)])

		return float(data.sum()) / len(data)

def searchForRule(cList, possible_rules):
	database = []
	for c in cList:
		for rule in possible_rules:
			database.append([(rule,c)])

	p = multiprocessing.Pool(multiprocessing.cpu_count())
	mapped = p.map(evaluateGame, database)

	#p.terminate()
	#mapped = p.map(printNum, database)

	#max_val1 = -100.0
	max_val1 = max(mapped)
	index1 = mapped.index(max_val1)
	print max_val1
	print index1

	#mapped = []
	#mapped = p.map(evaluateGame, database)
	#max_val2 = max(mapped)
	#index2 = mapped.index(max_val2) + 16000
	#print max_val2
	#print index2	

	#if max_val1 > max_val2:
	print str(database[index1][0][0][0]) + " and " + str(database[index1][0][0][1]) + " and " + str(database[index1][0][0][2]) + " and " + str(database[index1][0][0][3]) + " then " + database[index1][0][1]
	#else:
	#	print str(database[index2][0][0][0]) + " and " + str(database[index2][0][0][1]) + " and " + str(database[index2][0][0][2]) + " and " + str(database[index2][0][0][3]) + " then " + database[index2][0][1]

default_class = 'hit'
#classList = ['stand', 'double_down', 'split']
classList = ['stand', 'double_down']
rule_list = []

searchForRule(classList, loadRuleList('ruleset.csv'))
