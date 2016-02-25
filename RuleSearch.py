from Pblackjack import *

import math, operator
import pickle

import generatesampledb as sampledb

class DBEntry:
	def __init__(self, player_cards, dealer_card):
		self.player_cards = player_cards
		self.dealer_card = dealer_card
		self.classification = ("", 0.0)

#f = open('fulldatatable.csv', 'rb')
f = open('tabletable.csv', 'rb')

database = []

#for element in f:
try:
	while True:
		database.append(pickle.load(f))
except:
	pass

f.close()

#ruleSet = []

def findLessPrevalentClass(data, cList):
	lessPrevalent = ('', 0)
	classPrevalence = {}

	for c in cList:
		classPrevalence[c] = 0

	for d in data:
		if d.classification[0] in classPrevalence:
			classPrevalence[d.classification[0]] = classPrevalence[d.classification[0]] + 1

	for key in classPrevalence:
		if lessPrevalent[0] == '' or classPrevalence[key] < lessPrevalent[1]:
			lessPrevalent = (key, classPrevalence[key])

	return lessPrevalent

def returnDataFromClass(fulldata, targetClass):
	result = []
	for d in fulldata:
		if d.classification[0] == targetClass:
			result.append(d)

	return result

def fillPoints(data):
	cards = [('2', [2]), ('3', [3]), ('4', [4]), ('5', [5]), ('6', [6]), ('7', [7]), ('8', [8]), ('9', [9]), ('10', [10]), ('J', [10]), ('Q', [10]), ('K', [10]), ('A', [1, 11])]
	game = GameNode(deck=make_deck(8))
	
	for d in data:
		temp_hand = []
		for entry in d.player_cards:
			for card in game.deck:
				if card.name == entry:
					temp_hand.append(card)
					game.deck.remove(card)
					break
		game.hand = temp_hand

		temp_dealer_hand = []
		for card in game.deck:
			if card.name == d.dealer_card:
				temp_dealer_hand.append(card)
				game.deck.remove(card)
				break
		game.dealer_hand = temp_dealer_hand

		player_points = game.totalHandPoints(game.hand)
		dealer_points = game.totalHandPoints(game.dealer_hand)

		d.points = max([0] + [x for x in player_points if x < 22])
		d.dealer_points = max([0] + [x for x in dealer_points if x < 22])
'''
def findBestValueForParameter(data, targetClass, parameter, allPossibleValues):
	data_values = {}
	for value in allPossibleValues:
		data_values[value] = {}
		temp_data = findElementsWithCondition(data, parameter, (value, value))
		data_values[value]['n'] = len(temp_data)
		data_values[value]['n_plus'] = len(returnDataFromClass(temp_data, targetClass))

	currentBest = None

	for key in data_values:
		if currentBest == None:
			currentBest = key
		else:
			currentBest = compareRuleGain(currentBest, data_values[currentBest]['n'], data_values[currentBest]['n_plus'], key, data_values[key]['n'], data_values[key]['n_plus'])

	return currentBest
'''
def intersection(data1, data2):
	return set(data1) & set(data2)

def difference(data1, data2):
	return list(set(data1).difference(set(data2)))

def twoCopiesOfCard(hand):
	if hand[0] == hand[1]:
		return True

	return False

def findBestValueForParameter(data, targetClass, currentRuleData, parameter_list, operator_list, atribution_parameter=None, atribution_operators=None, alternate_parameter_list=None, alternate_operator_list=None):
	data_values = {}
	for (parameter, values) in parameter_list:
		data_values[parameter] = {}
		for value in values:
			data_values[parameter][value] = {}
			for operator in operator_list:
				data_values[parameter][value][operator] = {}
				data_values[parameter][value][operator]['data'] = findElementsWithCondition(data, parameter, operator, value)
				data_values[parameter][value][operator]['true_positives'] = returnDataFromClass(data_values[parameter][value][operator]['data'], targetClass)
				#temp_data = findElementsWithCondition(data, parameter, operator, value)
				data_values[parameter][value][operator]['n'] = len(data_values[parameter][value][operator]['data'])
				data_values[parameter][value][operator]['n_plus'] = len(returnDataFromClass(data_values[parameter][value][operator]['data'], targetClass))

	if alternate_parameter_list != None:
		for (parameter, values) in alternate_parameter_list:
			data_values[parameter] = {}
			for value in values:
				data_values[parameter][value] = {}
				for operator in alternate_operator_list:
					data_values[parameter][value][operator] = {}
					data_values[parameter][value][operator]['data'] = findElementsWithCondition(data, parameter, operator, value)
					data_values[parameter][value][operator]['true_positives'] = returnDataFromClass(data_values[parameter][value][operator]['data'], targetClass)
					#temp_data = findElementsWithCondition(data, parameter, operator, value)
					data_values[parameter][value][operator]['n'] = len(data_values[parameter][value][operator]['data'])
					data_values[parameter][value][operator]['n_plus'] = len(returnDataFromClass(data_values[parameter][value][operator]['data'], targetClass))

	bestRule = {}
	bestRule['gain'] = None
	bestRule['parameter'] = None
	bestRule['operator'] = None
	bestRule['value'] = None

	temp_gain = None

	for parameter in data_values:
		for value in data_values[parameter]:
			for operator in data_values[parameter][value]:
				if bestRule['gain'] == None:
					bestRule['gain'] = ruleGain(len(intersection(currentRuleData['true_positives'], data_values[parameter][value][operator]['true_positives'])), data_values[parameter][value][operator]['n_plus'], data_values[parameter][value][operator]['n'], currentRuleData['n_plus'], currentRuleData['n'])
					bestRule['parameter'] = parameter
					bestRule['operator'] = operator
					bestRule['value'] = value
					bestRule['class'] = targetClass
				else:
					temp_gain = ruleGain(len(intersection(currentRuleData['true_positives'], data_values[parameter][value][operator]['true_positives'])), data_values[parameter][value][operator]['n_plus'], data_values[parameter][value][operator]['n'], currentRuleData['n_plus'], currentRuleData['n'])
					#print temp_gain
					if temp_gain > bestRule['gain']:
						bestRule['gain'] = temp_gain
						bestRule['parameter'] = parameter
						bestRule['operator'] = operator
						bestRule['value'] = value
						bestRule['class'] = targetClass

	if atribution_parameter != None and atribution_parameter != [] and atribution_operators != []:
		for parameter in atribution_parameter:
			for operator in atribution_operators:
				temp_atr_data = findElementsWithAtribute(data, parameter, operator)
				temp_atr_true_positives = returnDataFromClass(temp_atr_data, targetClass)
				temp_atr_n = len(temp_atr_data)
				temp_atr_n_plus = len(temp_atr_true_positives)

				temp_gain = ruleGain(len(intersection(currentRuleData['true_positives'], temp_atr_true_positives)), temp_atr_n_plus, temp_atr_n, currentRuleData['n_plus'], currentRuleData['n'])
				
				if bestRule['gain'] == None or temp_gain > bestRule['gain']:
					bestRule['gain'] = temp_gain
					bestRule['parameter'] = parameter
					bestRule['operator'] = operator
					bestRule['value'] = None
					bestRule['class'] = targetClass

	#print "gain " + str(bestRule['gain'])
	return bestRule
	'''
	currentBestRule = None
	currentBest = None

	for parameter in data_values:
		for key in data_values[parameter]:
			if currentBest == None:
				currentBest = key
				currentBestRule = parameter
			else:
				currentBestRule, currentBest = compareRuleGain((currentBestRule, currentBest), data_values[currentBestRule][currentBest]['n'], data_values[currentBestRule][currentBest]['n_plus'], (parameter, key), data_values[parameter][key]['n'], data_values[parameter][key]['n_plus'])

	return (currentBestRule, currentBest)
	'''

def findAllValuesForParameter(data, parameter):
	values = []

	for d in data:
		dDict = d.__dict__

		if dDict[parameter] not in values:
			values.append(dDict[parameter])

	return values

def findDiscreetRule(data, parameter):
	player_max_points = None
	player_min_points = None
	
	for d in data:
		dDict = d.__dict__
		if player_max_points == None or dDict[parameter] > player_max_points:
			player_max_points = dDict[parameter]
		if player_min_points == None or dDict[parameter] < player_min_points:
			player_min_points = dDict[parameter]

	#print "if points >= " + str(player_min_points) + " and points <= " + str(player_max_points) + " then STAND"

	return (player_min_points, player_max_points)
'''
def findElementsWithCondition(data, parameter, minmax):
	result = []

	for d in data:
		dataDict = d.__dict__

		if dataDict[parameter] >= minmax[0] and dataDict[parameter] <= minmax[1]:
			result.append(d)

	return result
'''

def findElementsWithCondition(data, parameter, operator, value):
	result = []

	for d in data:
		dataDict = d.__dict__

		if operator(dataDict[parameter], value):
			result.append(d)

	return result

def findElementsWithAtribute(data, parameter, operator):
	result = []

	for d in data:
		dataDict = d.__dict__

		#if dataDict[parameter] >= minmax[0] and dataDict[parameter] <= minmax[1]:
		if operator(dataDict[parameter]):
			result.append(d)

	return result

def findElementsForRule(data, rule):
	temp_data = data

	result = []

	for condition in rule:
		result = []
		for d in temp_data:
			dataDict = d.__dict__

			#if dataDict[parameter] >= minmax[0] and dataDict[parameter] <= minmax[1]:
			if condition['value'] != None:
				if condition['operator'](dataDict[condition['parameter']], condition['value']):
					result.append(d)
			else:
				if condition['operator'](dataDict[condition['parameter']]):
					result.append(d)

		temp_data = result

	return result

def findNegativeElements(data, rule_list):
	negative_elements = []
	temp_elements = []
	
	db = copy.copy(data)
	
	for rule in rule_list:
		temp_elements = findElementsForRule(db, rule)
		negative_elements.extend(difference(temp_elements, returnDataFromClass(temp_elements, rule[0]['class'])))
		db = difference(db, temp_elements)
	
	return negative_elements
'''
def compareRuleGain(rule1, n_plus, n, rule2, ni_plus, ni):
	gain = math.log(float(ni_plus) / float(ni), 2) - math.log(float(n_plus) / float(n))

	if gain > 0:
		return rule2

	return rule1
'''
def removeValueFromParameterList(parameter_list, parameter, value):
	for (par, values) in parameter_list:
		if par == parameter:
			if value in values:
				temp_par = par
				temp_values = values
				temp_values.remove(value)

				parameter_list.remove((par, values))
				parameter_list.append((temp_par, temp_values))

				break

	pass

def ruleGain(s, ni_plus, ni, n_plus, n):
	if s == 0:
		return 0.0
	if n_plus == 0:
		if ni_plus == 0:
			return 0.0
		return -1.0 * float(ni_plus) * math.log(float(ni_plus) / float(ni), 2)
	return float(s) * (math.log(float(ni_plus) / float(ni), 2) - math.log(float(n_plus) / float(n), 2))
'''
def ruleGain(rule1, rule2):
	s = len(intersection(rule1['true_positives'], rule2['true_positives']))
	ni_plus = rule1['n_plus']
	ni = rule1['n']
	n_plus = rule2['n_plus']
	n = rule2['n']

	if s == 0:
		return 0.0
	if n_plus == 0:
		return float(ni_plus) * (math.log(float(ni_plus) / float(ni)) - 1.0)
	return float(s) * (math.log(float(ni_plus) / float(ni), 2) - math.log(float(n_plus) / float(n)))
'''

def ruleDataInfo(data, targetClass, ruleInfo):
	result = {}
	result['n'] = None
	result['n_plus'] = None
	result['true_positives'] = None

	temp_data = data
	
	if ruleInfo == None:
		result['n'] = len(data)
		result['n_plus'] = 0
		result['true_positives'] = data
	else:
		#for rule in ruleInfo:
		#	temp_data = findElementsWithCondition(temp_data, rule['parameter'], rule['operator'], rule['value'])
		temp_data = findElementsForRule(temp_data, ruleInfo)

		result['n'] = len(temp_data)
		result['true_positives'] = returnDataFromClass(temp_data, targetClass)
		result['n_plus'] = len(result['true_positives'])

	return result

def grow(growdb, targetClass):
	classdata = []

	classdata = returnDataFromClass(growdb, targetClass)

	currentRule = []

	possible_parameters = ['points', 'dealer_points']
	possible_operators = [operator.le, operator.ge]

	alternate_parameters = ['player_cards']
	alternate_parameters_values = [('player_cards', ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"])]
	alternate_operators = [operator.contains]

	atribution_parameters = ['player_cards']
	atribution_operators = [twoCopiesOfCard]
	#possible_atribution_values = [('player_cards', [True])]

	possible_parameters_values = []
	for parameter in possible_parameters:
		if parameter == 'points':
			possible_parameters_values.append((parameter, [x for x in range(4, 22)]))
		if parameter == 'dealer_points':
			possible_parameters_values.append((parameter, [x for x in range(3, 12)]))
		#possible_parameters_values.append((parameter, findAllValuesForParameter(classdata, parameter)))

	currentRuleInfo = ruleDataInfo(growdb, targetClass, None)
	currentRule = []

	while True:
		if currentRule == []:
			bestRule = findBestValueForParameter(growdb, targetClass, currentRuleInfo, possible_parameters_values, possible_operators, atribution_parameters, atribution_operators, alternate_parameters_values, alternate_operators)
		else:
			bestRule = findBestValueForParameter(findElementsForRule(growdb, currentRule), targetClass, currentRuleInfo, possible_parameters_values, possible_operators, atribution_parameters, atribution_operators, alternate_parameters_values, alternate_operators)

		if bestRule['operator'] == None:
			break

		currentRule.append(bestRule)
		currentRuleInfo = ruleDataInfo(growdb, targetClass, currentRule)

		#printRule(currentRule)
		#print str(currentRuleInfo['n']) + "    " + str(currentRuleInfo['n_plus'])

		if currentRuleInfo['n'] == currentRuleInfo['n_plus']:
			break

		if bestRule['parameter'] in possible_parameters:
			removeValueFromParameterList(possible_parameters_values, bestRule['parameter'], bestRule['value'])
		elif bestRule['parameter'] in alternate_parameters:
			removeValueFromParameterList(alternate_parameters_values, bestRule['parameter'], bestRule['value'])
		else:
			atribution_parameters = None
			atribution_operators = None

	#printRule(currentRule)

	return currentRule

def grow_i(growdb, targetClass, rule):
	classdata = []

	classdata = returnDataFromClass(growdb, targetClass)

	currentRule = []

	possible_parameters = ['points', 'dealer_points', 'hand']
	possible_operators = [operator.le, operator.ge]

	atribution_parameters = ['player_cards']
	atribution_operators = [twoCopiesOfCard]

	possible_parameters_values = []
	for parameter in possible_parameters:
		if parameter == 'points':
			possible_parameters_values.append((parameter, [x for x in range(4, 22)]))
		if parameter == 'dealer_points':
			possible_parameters_values.append((parameter, [x for x in range(3, 12)]))
		#possible_parameters_values.append((parameter, findAllValuesForParameter(classdata, parameter)))

	for condition in rule:
		removeValueFromParameterList(possible_parameters_values, condition['parameter'], condition['value'])
	
	currentRuleInfo = ruleDataInfo(growdb, targetClass, rule)
	currentRule = copy.copy(rule)

	while True:
		if currentRule == []:
			bestRule = findBestValueForParameter(growdb, targetClass, currentRuleInfo, possible_parameters_values, possible_operators, atribution_parameters, atribution_operators)
		else:
			bestRule = findBestValueForParameter(findElementsForRule(growdb, currentRule), targetClass, currentRuleInfo, possible_parameters_values, possible_operators, atribution_parameters, atribution_operators)

		if bestRule['operator'] == None:
			break

		currentRule.append(bestRule)
		currentRuleInfo = ruleDataInfo(growdb, targetClass, currentRule)

		#printRule(currentRule)
		#print str(currentRuleInfo['n']) + "    " + str(currentRuleInfo['n_plus'])

		if currentRuleInfo['n'] == currentRuleInfo['n_plus']:
			break

		if atribution_parameters == None or bestRule['parameter'] not in atribution_parameters:
			removeValueFromParameterList(possible_parameters_values, bestRule['parameter'], bestRule['value'])
		else:
			atribution_parameters = None
			atribution_operators = None
		#removeValueFromParameterList(possible_parameters_values, bestRule['parameter'], bestRule['value'])

	#printRule(currentRule)

	return currentRule
	
def printRule(cRule, targetClass=None):
	ruleString = "if "
	for condition in cRule:
		if condition['value'] != None:
			if condition['operator'] == operator.contains:
				ruleString = ruleString + condition['parameter'] + " has " + condition['value'] + " and "
				#ruleString = ruleString + condition['value'] + " in " + condition['parameter'] + " and "
			else:
				ruleString = ruleString + condition['parameter']
				ruleString = ruleString + (" >= " if condition['operator'] == operator.ge else " <= ")
				ruleString = ruleString + str(condition['value']) + " and "
		else:
			ruleString = ruleString + "twoCopiesOfCard(" + condition['parameter'] + ") and "

	ruleString = ruleString[:-4] + "then " + cRule[0]['class']

	if targetClass != None:
		ruleString = ruleString + " " + targetClass

	print ruleString

def ruleValueMetric(ruleInfo):
	p = ruleInfo['n_plus']
	n = ruleInfo['n'] - p

	#return float(p - n) / float(p + n)
	return float(p + 1) / float(p + n + 2)

def prune(prunedb, targetClass, rule):
	if len(rule) < 2:
		return rule

	ruleInfo = ruleDataInfo(prunedb, targetClass, rule)
	rvm_currentRule = ruleValueMetric(ruleInfo)

	ruleInfo = ruleDataInfo(prunedb, targetClass, rule[:-1])
	rvm_optionalRule = ruleValueMetric(ruleInfo)

	if rvm_currentRule >= rvm_optionalRule:
		return rule
	else:
		return prune(prunedb, targetClass, rule[:-1])
	
def prune_i(prunedb, targetClass, rule, ruleList):
	if len(rule) < 2:
		return rule
	
	#for x in findNegativeElements(prunedb, ruleList):
	#	print "neg: " + str(x.player_cards) + " " + str(x.dealer_card) + " " + str(x.classification)
	rvm_currentRule = ruleComparisonMetric(len(findNegativeElements(prunedb, ruleList)), len(prunedb))
		
	r_index = ruleList.index(rule)
	temp_ruleList = ruleList[:r_index] + [rule[:-1]] + ruleList[r_index+1:]
	rvm_optionalRule = ruleComparisonMetric(len(findNegativeElements(prunedb, temp_ruleList)), len(prunedb))
	
	if rvm_currentRule <= rvm_optionalRule:
		return rule
	else:
		return prune_i(prunedb, targetClass, rule[:-1], temp_ruleList)

def removeRedundantRules(database, ruleList):
	rules_to_be_removed = []

	for r1 in ruleList:
		r1_elements = []
		r1_elements = findElementsForRule(database, r1)
		for r2 in ruleList:
			r2_elements = []
			r2_elements = findElementsForRule(database, r2)
			if r1 != r2 and r1[0]['class'] == r2[0]['class'] and r1 not in rules_to_be_removed:
				intersect = []
				intersect = intersection(r1_elements, r2_elements)
				#print "i: " +  str(len(intersect)) + " r1l: " + str(len(r1_elements)) + " r2l: " + str(len(r2_elements))
				if len(intersect) == len(r1_elements):
					#print 'a'
					rules_to_be_removed.append(r1)

	for rr in rules_to_be_removed:
		ruleList.remove(rr)

def removeRedunancyFromRules(database, rule_list):
	for rule in rule_list:
		removeRedundantConditions(database, rule)

def removeRedundantConditions(database, rule):
	rule_copy = copy.copy(rule)
	number_of_elements_rule = len(findElementsForRule(database, rule))
	conditions_remove = []
	
	for condition in rule:
		temp_elem_size = 0
		rule_copy = copy.copy(rule)
		rule_copy.remove(condition)
		temp_elem_size = len(findElementsForRule(database, rule_copy))
		if temp_elem_size == number_of_elements_rule:
			conditions_remove.append(condition)
	
	for rcondition in conditions_remove:
		rule.remove(rcondition)

def compareConditions(cx, cy):
	priority_list = {'parameter': ['player_cards', 'points', 'dealer_points'], 'operator': [operator.ge, operator.le, operator.contains]}

	if cx['parameter'] == cy['parameter']:
		return priority_list['operator'].index(cx['operator']) - priority_list['operator'].index(cy['operator'])

	return priority_list['parameter'].index(cx['parameter']) - priority_list['parameter'].index(cy['parameter'])

def orderConditions(rList):
	temp_rlist = []
	for rule in rList:
		temp_rlist.append(sorted(rule, cmp=compareConditions))

	return temp_rlist
'''
def orderConditions(rule, pList):
	conditions_dict = {}
	for condition in rule:
		if condition['parameter'] not in conditions_dict:
			conditions_dict[condition['parameter']] = {}
		if condition['operator'] not in conditions_dict[condition['parameter']]:
			conditions_dict[condition['parameter']][condition['operator']] = condition	

	print conditions_dict
'''

def ruleComparisonMetric(negatives, total):
	# (TOTAL POSITIVES - TOTAL NEGATIVES) / (POSITIVES - NEGATIVES)
	return float(float(negatives) / float(total))

def generateAlternateRule(grow_database, prune_database, targetClass, rList):
	r = grow(grow_database, targetClass)
	r = prune_i(prune_database, targetClass, r, [r] + rList[1:])

	#for condition in r:
	#	condition['class'] = targetClass

	return r

def generateRevisedRule(grow_database, prune_database, targetClass, rule, rList):
	r = grow_i(grow_database, targetClass, rule)
	r = prune_i(prune_database, targetClass, rule, rList)

	#for condition in r:
	#	condition['class'] = targetClass
		
	return r

def fullRuleListEntropy(data, rule_list, class_list):
	db = copy.copy(data)
	sum = 0.0

	for rule in rule_list:
		temp_elements = findElementsForRule(db, rule)
		true_positive_elements = returnDataFromClass(temp_elements, rule[0]['class'])
		sum = sum +	ruleGain(1, len(true_positive_elements), len(temp_elements), 0, 0)

		db = difference(db, temp_elements)
		if rule[0]['class'] in class_list:
			class_list.remove(rule[0]['class'])
	
	temp_elements = db
	true_positive_elements = returnDataFromClass(temp_elements, class_list[0])
	sum = sum +	ruleGain(1, len(true_positive_elements), len(temp_elements), 0, 0)
	
	return sum

def learnRuleSet(db, cList, rlist):
	#grow_database, prune_database = sampledb.loadWithRandomSamples(db)
	grow_database, prune_database = sampledb.loadWithRandomSamplesByClass(db, cList)
	
	lpClass = findLessPrevalentClass(db, cList)

	r = grow(grow_database, lpClass[0])
	r = prune(prune_database, lpClass[0], r)

	for condition in r:
		condition['class'] = lpClass[0]

	if len(returnDataFromClass(findElementsForRule(db, r), lpClass[0])) <= 0:
		classList.remove(lpClass[0])
	else:
		printRule(r, lpClass[0])

		rlist.append(r)

		print "correct elements " +  str(len(returnDataFromClass(findElementsForRule(db, r), lpClass[0])))
		print "total elements " +  str(len(findElementsForRule(db, r)))
	
		db = difference(db, findElementsForRule(db, r))

		print "length: " +  str(len(returnDataFromClass(db, lpClass[0])))

		if len(returnDataFromClass(db, lpClass[0])) <= 0:
			classList.remove(lpClass[0])

	#for c in db:
	#	print str(c.player_cards) + "   " + str(c.dealer_card) + "   " + str(c.classification) + "   " + str(c.points) + "   " + str(c.dealer_points)

	if len(classList) > 1:
		learnRuleSet(db, classList, rlist)
	else:
		print "right: " + str(len(returnDataFromClass(db, classList[0])))
		print "left:  " + str(len(db))
		print classList[0]

def optimizeRuleSet(db, cList, rList):
	grow_database, prune_database = sampledb.loadWithRandomSamplesByClass(db, cList)
	
	print "-----------------------------"
		
	for rule in rList:
		rule_index = rList.index(rule)
		printRule(rule)
		originalRuleEntropy = fullRuleListEntropy(db, rList, cList)
		
		rAlt = generateAlternateRule(grow_database, prune_database, rule[0]['class'], rList)
		alternateRuleEntropy = fullRuleListEntropy(db, rList[:rule_index] + [rAlt] + rList[rule_index+1:], cList)
		print "Alt: "
		printRule(rAlt)
		rRev = generateRevisedRule(grow_database, prune_database, rule[0]['class'], rule, rList)
		revisedRuleEntropy = fullRuleListEntropy(db, rList[:rule_index] + [rRev] + rList[rule_index+1:], cList)
		print "Rev: "
		printRule(rRev)
		
		print "Org: " + str(originalRuleEntropy) + " Alt: " + str(alternateRuleEntropy) + " Rev: " + str(revisedRuleEntropy)
		max_value = max([originalRuleEntropy, alternateRuleEntropy, revisedRuleEntropy])
		
		if max_value == alternateRuleEntropy and alternateRuleEntropy != originalRuleEntropy:
			rList = rList[:rule_index] + [rAlt] + rList[rule_index+1:]
		if max_value == revisedRuleEntropy and revisedRuleEntropy != originalRuleEntropy:
			rList = rList[:rule_index] + [rRev] + rList[rule_index+1:]		

def Ripper(database, cList, rList, k):
	learnRuleSet(copy.copy(database), copy.copy(cList), rList)
	removeRedunancyFromRules(database, rList)
	#for i in range(0, k):
	#	optimizeRuleSet(copy.copy(database), copy.copy(cList), rList)

	removeRedundantRules(database, rList)

def accuracy(data, class_list, rList):
	db = copy.copy(data)
	cList = copy.copy(class_list)
	number_of_negative = 0
	
	for rule in rList:
		temp_elements = findElementsForRule(db, rule)
		positive_elements = returnDataFromClass(temp_elements, rule[0]['class'])
		number_of_negative = number_of_negative + len(temp_elements) - len(positive_elements)
		db = difference(db, temp_elements)
	
		if rule[0]['class'] in cList:
			cList.remove(rule[0]['class'])
	
	temp_elements = db
	positive_elements = returnDataFromClass(temp_elements, cList[0])
	number_of_negative = number_of_negative + len(temp_elements) - len(positive_elements)
	
	print number_of_negative
	
	return 1.0 - float(float(number_of_negative) / float(len(data)))

def accuracyRatioPerRule(data, class_list, rList):
	db = copy.copy(data)
	cList = copy.copy(class_list)

	for rule in rList:
		if rule[0]['class'] in cList:
			cList.remove(rule[0]['class'])

	defaultClass = cList[0]

	print len(returnDataFromClass(db, defaultClass))

	db = copy.copy(data)

	positives = 0

	for rule in rList:
		temp_db = findElementsForRule(db, rule)
		positives = positives + len(returnDataFromClass(temp_db, rule[0]['class']))
		db = difference(db, temp_db)
		printRule(rule)
		print positives + len(returnDataFromClass(db, defaultClass))


#learnRuleSet(copy.copy(database), classList, rule_list)

#print len(returnDataFromClass(database, 'double_down'))
#print len(returnDataFromClass(database, 'stand'))
#print len(returnDataFromClass(database, 'hit'))

#for r in rule_list:
#	printRule(r)

#removeRedundantRules(database, rule_list)

#print "---------------------------------------------------"

#for r in rule_list:
#	printRule(r)

#removeRedunancyFromRules(database, rule_list)

#print "---------------------------------------------------"

#for r in rule_list:
#	printRule(r)

#optimizeRuleSet(copy.copy(database), ['stand', 'hit', 'double_down'], rule_list)

#removeRedundantRules(database, rule_list)
fillPoints(database)
classList = ['stand', 'hit', 'double_down', 'split']
rule_list = []

Ripper(database, classList, rule_list, 10)

#print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/"

#for r in rule_list:
#	printRule(r)


print "/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\"

#rule_list = orderConditions(rule_list)

for r in rule_list:
	printRule(r)

print accuracy(database, classList, rule_list)

print "\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/"

accuracyRatioPerRule(database, classList, rule_list)

#for c in findElementsForRule(database, r):
#	print str(c.player_cards) + "   " + str(c.dealer_card) + "   " + str(c.classification) + "   " + str(c.points) + "   " + str(c.dealer_points)

'''
print 'rvm ' + str(ruleValueMetric(ruleDataInfo(database, lpClass[0], currentRule)))
print 'rvm ' + str(ruleValueMetric(ruleDataInfo(database, lpClass[0], currentRule[:-1])))

#temp = findElementsWithCondition(database, rule, ruleBoundries)

#rule = 'dealer_points'
#ruleBoundries = findDiscreetRule(classdata, rule)
#currentRule.append((rule, ruleBoundries))

ruleString = "if "

for rule in currentRule:
	ruleString = ruleString + rule['parameter']
	ruleString = ruleString + " >= " if rule['operator'] == operator.ge else " <= "
	ruleString = ruleString + str(rule['value']) + " and "

ruleString = ruleString[:-4] + "then STAND"

print ruleString

print len(classdata)
print len(findElementsForRule(classdata, currentRule))
print len(findElementsForRule(database, currentRule))
#print len(findElementsWithCondition(classdata, rule['parameter'], rule['operator'], rule['value']))
#print len(findElementsWithCondition(database, rule['parameter'], rule['operator'], rule['value']))

#
#for c in classdata:
#	print str(c.player_cards) + "   " + str(c.dealer_card) + "   " + str(c.classification) + "   " + str(c.points) + "   " + str(c.dealer_points)

print "---------------"

for c in findElementsForRule(database, currentRule):
	print str(c.player_cards) + "   " + str(c.dealer_card) + "   " + str(c.classification) + "   " + str(c.points) + "   " + str(c.dealer_points)
'''
