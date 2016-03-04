from Pblackjack import *

import operator
import pickle
import pandas as pd

import multiprocessing

import time

class RuleCondition:
	def __init__(self, parameter, operator, value):
		self.parameter = parameter
		self.operator = operator
		self.value = value

	def __str__(self):
		oper = "<=" if self.operator == operator.le else ">="
		return self.parameter + " " + oper + " " + str(self.value)

class Counter(object):
    def __init__(self):
        self.val = multiprocessing.Value('i', 0)

    def increment(self, n=1):
        with self.val.get_lock():
            self.val.value += n

    @property
    def value(self):
        return self.val.value


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
	c.increment()
	print c.value
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
	start_time = time.time()

	database = []
	i = 0
	for c in cList:
		for rule in possible_rules:
			database.append([(rule,c)])
			i = i + 1

	rule_set = database[8534]
	temp_db = []

	for l in database:
		temp = copy.copy(rule_set)
		temp.extend(l)
		temp_db.append(temp)

	database = copy.copy(temp_db)

	p = multiprocessing.Pool(multiprocessing.cpu_count())
	mapped = p.map(evaluateGame, database)

	print("--- %s seconds ---" % (time.time() - start_time))

	max_val1 = max(mapped)
	index1 = mapped.index(max_val1)
	print max_val1
	print index1

	for i in range(0, 2):
		print str(database[index1][i][0][0]) + " and " + str(database[index1][i][0][1]) + " and " + str(database[index1][i][0][2]) + " and " + str(database[index1][i][0][3]) + " then " + database[index1][i][1]

	p.close()

c = Counter()

default_class = 'hit'
#classList = ['stand', 'double_down', 'split']
classList = ['stand', 'double_down']
rule_list = []

searchForRule(classList, loadRuleList('ruleset.csv'))
