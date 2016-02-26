import operator
import pickle

f = open('ruleset.csv', 'wb')
f2 = open('ruleset.txt', 'w')

class RuleCondition:
	def __init__(self, parameter, operator, value):
		self.parameter = parameter
		self.operator = operator
		self.value = value

	def __str__(self):
		oper = "<=" if self.operator == operator.le else ">="
		return self.parameter + " " + oper + " " + str(self.value)

def generateRules(parameter_list, operator_list, n):
	pList = {}
	possible_rules = []
	temp_list = []
	for (parameter, values) in parameter_list:
		pList[parameter] = values
		for value in values:
			for oper in operator_list:
				temp_list.append(RuleCondition(parameter, oper, value))

		temp_r = [[x] + [y] for x in temp_list for y in temp_list if x.parameter == y.parameter and x.operator != y.operator]

	elements_remove = []
	for i in range(0, len(temp_r)):
		for j in range(i+1, len(temp_r)):
			if temp_r[i][0].parameter == temp_r[j][1].parameter and temp_r[i][0].operator == temp_r[j][1].operator and temp_r[i][0].value == temp_r[j][1].value:
				if temp_r[j] not in elements_remove:
					elements_remove.append(temp_r[j])

	for elem in elements_remove:
		temp_r.remove(elem)

	elements_remove = []
	for x in temp_r:
		if x[0].operator == operator.le and x[0].value < x[1].value:
			elements_remove.append(x)
		if x[1].operator == operator.le and x[1].value < x[0].value:
			elements_remove.append(x)

	for elem in elements_remove:
		temp_r.remove(elem)

	temp_list = [[x[0] , x[1], y[0], y[1]] for x in temp_r for y in temp_r if x[0].parameter == 'points' and y[0].parameter == 'dealer_points']

	for r in temp_list:
		pickle.dump(r, f)
		f2.write(str(r[0]) + " and " + str(r[1]) + " and " + str(r[2]) + " and " + str(r[3]) + '\n')

	#for r in temp_list:
	#	print str(r[0]) + " and " + str(r[1]) + " and " + str(r[2]) + " and " + str(r[3])

def searchForAllRules():
	currentRule = []

	possible_parameters = ['points', 'dealer_points']
	possible_operators = [operator.le, operator.ge]

	possible_parameters_values = []
	for parameter in possible_parameters:
		if parameter == 'points':
			possible_parameters_values.append((parameter, [x for x in range(4, 22)]))
		if parameter == 'dealer_points':
			possible_parameters_values.append((parameter, [x for x in range(2, 12)]))

	generateRules(possible_parameters_values, possible_operators, 0)

searchForAllRules()

f.close()
f2.close()