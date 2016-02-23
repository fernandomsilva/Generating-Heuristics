from Pblackjack import *
#import pandas as pd
import pickle, json

def blackjackTable(playerHand, playerPoints, dealerHand, dealerPoints):
    table = {}
    table['17+'] = {'2': 'st', '3':'st', '4': 'st', '5': 'st', '6': 'st', '7': 'st', '8': 'st', '9': 'st', '10': 'st', 'A': 'st'}
    table['16'] = {'2': 'st', '3':'st', '4': 'st', '5': 'st', '6': 'st', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['15'] = {'2': 'st', '3':'st', '4': 'st', '5': 'st', '6': 'st', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['14'] = {'2': 'st', '3':'st', '4': 'st', '5': 'st', '6': 'st', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['13'] = {'2': 'st', '3':'st', '4': 'st', '5': 'st', '6': 'st', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['12'] = {'2': 'ht', '3':'ht', '4': 'st', '5': 'st', '6': 'st', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['11'] = {'2': 'dd', '3':'dd', '4': 'dd', '5': 'dd', '6': 'dd', '7': 'dd', '8': 'dd', '9': 'dd', '10': 'dd', 'A': 'ht'}
    table['10'] = {'2': 'dd', '3':'dd', '4': 'dd', '5': 'dd', '6': 'dd', '7': 'dd', '8': 'dd', '9': 'dd', '10': 'ht', 'A': 'ht'}
    table['9'] = {'2': 'ht', '3':'dd', '4': 'dd', '5': 'dd', '6': 'dd', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['8'] = {'2': 'ht', '3':'ht', '4': 'ht', '5': 'ht', '6': 'ht', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['7'] = {'2': 'ht', '3':'ht', '4': 'ht', '5': 'ht', '6': 'ht', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['6'] = {'2': 'ht', '3':'ht', '4': 'ht', '5': 'ht', '6': 'ht', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['5'] = {'2': 'ht', '3':'ht', '4': 'ht', '5': 'ht', '6': 'ht', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['A,10'] = {'2': 'st', '3':'st', '4': 'st', '5': 'st', '6': 'st', '7': 'st', '8': 'st', '9': 'st', '10': 'st', 'A': 'st'}
    table['A,9'] = {'2': 'st', '3':'st', '4': 'st', '5': 'st', '6': 'st', '7': 'st', '8': 'st', '9': 'st', '10': 'st', 'A': 'st'}
    table['A,8'] = {'2': 'st', '3':'st', '4': 'st', '5': 'st', '6': 'st', '7': 'st', '8': 'st', '9': 'st', '10': 'st', 'A': 'st'}
    table['A,7'] = {'2': 'st', '3':'dd', '4': 'dd', '5': 'dd', '6': 'dd', '7': 'st', '8': 'st', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['A,6'] = {'2': 'ht', '3':'dd', '4': 'dd', '5': 'dd', '6': 'dd', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['A,5'] = {'2': 'ht', '3':'ht', '4': 'dd', '5': 'dd', '6': 'dd', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['A,4'] = {'2': 'ht', '3':'ht', '4': 'dd', '5': 'dd', '6': 'dd', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['A,3'] = {'2': 'ht', '3':'ht', '4': 'ht', '5': 'dd', '6': 'dd', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['A,2'] = {'2': 'ht', '3':'ht', '4': 'ht', '5': 'dd', '6': 'dd', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['A,A'] = {'2': 'sp', '3':'sp', '4': 'sp', '5': 'sp', '6': 'sp', '7': 'sp', '8': 'sp', '9': 'sp', '10': 'sp', 'A': 'sp'}
    table['8,8'] = {'2': 'sp', '3':'sp', '4': 'sp', '5': 'sp', '6': 'sp', '7': 'sp', '8': 'sp', '9': 'sp', '10': 'sp', 'A': 'sp'}
    table['10,10'] = {'2': 'st', '3':'st', '4': 'st', '5': 'st', '6': 'st', '7': 'st', '8': 'st', '9': 'st', '10': 'st', 'A': 'st'}
    table['9,9'] = {'2': 'sp', '3':'sp', '4': 'sp', '5': 'sp', '6': 'sp', '7': 'st', '8': 'sp', '9': 'sp', '10': 'st', 'A': 'st'}
    table['7,7'] = {'2': 'sp', '3':'sp', '4': 'sp', '5': 'sp', '6': 'sp', '7': 'sp', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['6,6'] = {'2': 'sp', '3':'sp', '4': 'sp', '5': 'sp', '6': 'sp', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['5,5'] = {'2': 'dd', '3':'dd', '4': 'dd', '5': 'dd', '6': 'dd', '7': 'dd', '8': 'dd', '9': 'dd', '10': 'ht', 'A': 'ht'}
    table['4,4'] = {'2': 'ht', '3':'ht', '4': 'ht', '5': 'sp', '6': 'sp', '7': 'ht', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['3,3'] = {'2': 'sp', '3':'sp', '4': 'sp', '5': 'sp', '6': 'sp', '7': 'sp', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}
    table['2,2'] = {'2': 'sp', '3':'sp', '4': 'sp', '5': 'sp', '6': 'sp', '7': 'sp', '8': 'ht', '9': 'ht', '10': 'ht', 'A': 'ht'}

    translation = {'st': 'stand', 'dd': 'double_down', 'sp': 'split', 'ht': 'hit'}
    
    dealerIndex = '10' if dealerPoints == 10 else dealerHand[0].name
    
    #print "P.hand: " + str([x.name + x.suit for x in playerHand]) + " P.points: " + str(playerPoints)
    #print "D.hand: " + str([x.name + x.suit for x in dealerHand]) + " D.points: " + str(dealerPoints)

    if len(playerHand) == 2:
        if playerHand[0].value == playerHand[1].value and playerHand[0].name != 'A':
            return translation[table[str(playerHand[0].value[0]) + ',' + str(playerHand[0].value[0])][dealerIndex]]
        elif playerHand[0].name == 'A' and playerHand[1].name == 'A':
            return translation[table['A,A'][dealerIndex]]
        elif playerHand[0].name == 'A':
            return translation[table['A,' + str(playerHand[1].value[0])][dealerIndex]]
        elif playerHand[1].name == 'A':
            return translation[table['A,' + str(playerHand[0].value[0])][dealerIndex]]
        else:
            if playerPoints < 17:
                return translation[table[str(playerPoints)][dealerIndex]]
            else:
                return translation[table['17+'][dealerIndex]]
    else:
        if playerPoints < 17:
            return translation[table[str(playerPoints)][dealerIndex]]
        else:
            return translation[table['17+'][dealerIndex]]

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
'''
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
'''
f = open('tabletable.csv', 'wb')
f2 = open('ttable.txt', 'w')

for i in range(0, len(database)):
	#all_moves = ['stand', 'hit', 'double_down']
	best = (None, None)
	#for m in all_moves:
	game = GameNode(deck=make_deck(8))
	setupGameWithEntry(game, database[i])
	#print blackjackTable(game.hand, game.points, game.dealer_hand, game.dealer_points)
	current = blackjackTable(game.hand, max([0] + [y for y in game.points if y < 22]), game.dealer_hand, max([0] + [y for y in game.dealer_points if y < 22]))
	#current = evaluateGame(m, database[i], 100000)
	
	#if best[1] == None or best[1] < current:
	best = (current, current)

	database[i].classification = copy.copy(best)

	pickle.dump(database[i], f)
	json.dump(database[i].__dict__, f2)

	print i

f.close()
f2.close()