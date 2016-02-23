import copy, random

class Card:
	def __init__(self, name, value, suit, hidden=False):
		self.name = name
		self.value = value
		self.suit = suit
		self.hidden = hidden

def make_deck(n=4):
	suits = ['C', 'D', 'H', 'S']
	cards = [('2', [2]), ('3', [3]), ('4', [4]), ('5', [5]), ('6', [6]), ('7', [7]), ('8', [8]), ('9', [9]),
				('10', [10]), ('J', [10]), ('Q', [10]), ('K', [10]), ('A', [1, 11])]
	deck = []
	deck = [Card(name, value, suit) for (name, value) in cards for suit in suits]
	for i in range(1, n):
		deck.extend(deck)

	return deck

class GameNode:
	def __init__(self, deck=make_deck(), hand=[], points=0, dealer_hand=[], dealer_points=0, split_hand=[], split_points=0, split_done=False, level=0, movein=[], split_movein=[]):
		self.deck = copy.copy(deck)
		self.hand = hand
		self.points = points
		self.dealer_hand = dealer_hand
		self.dealer_points = dealer_points
		self.split_hand = split_hand
		self.split_points = split_points
		self.split_done = split_done
		self.level = level
		self.movein = movein
		self.split_movein = split_movein
		self.moves = []
		self.children = []
		self.result = None

	def spawn(self):
		node = GameNode(self.deck, copy.copy(self.hand), self.points, copy.copy(self.dealer_hand), self.dealer_points, self.split_hand, self.split_points, self.split_done, self.level, copy.copy(self.movein), copy.copy(self.split_movein))
		node.result = self.result

		return node
	
	def showNode(self):
		print "P.hand: " + str([x.name + x.suit for x in self.hand]) + " P.points: " + str(self.points)
		print "D.hand: " + str([x.name + x.suit for x in self.dealer_hand]) + " D.points: " + str(self.dealer_points)
	
		return

	def drawCard(self, hidden=False):
		card = random.choice(self.deck)
		self.deck.remove(card)
		card.hidden = hidden

		return card

	def setup(self):
		self.hand = [self.drawCard(), self.drawCard()]
		self.points = self.totalHandPoints(self.hand)

		#self.dealer_hand = [self.drawCard(), self.drawCard(True)]
		self.dealer_hand = [self.drawCard()]
		self.dealer_points = self.totalHandPoints(self.dealer_hand)
		
		self.split_hand = []
		self.split_points = 0
		self.split_done = False
		
		self.movein = []
		self.split_movein = []
		
		self.moves = self.possible_moves()

		return

	def findnode(self, move):
		for child in self.children:
			if child.movein == move:
				return child

		return None

	def getmoves(self):
		if not self.moves:
			self.setmoves()
		return self.moves

	def totalHandPoints(self, hand):
		temp = [c.value for c in hand if c.hidden == False]
		cardPoints = [0]
		cardSinglePoints = 0

		for value in temp:
			if len(value) == 1:
				cardSinglePoints = cardSinglePoints + value[0]
				temp.remove(value)

		cardPoints[0] = cardSinglePoints

		for double_value in temp:
			aux = copy.copy(cardPoints)
	
			for points in aux:
				temp_points = points
				cardPoints.remove(points)

				for value in double_value:
					cardPoints.append(temp_points + value)

		return list(set(cardPoints))

	def dealerPlays(self):
		for card in self.dealer_hand:
			card.hidden = False

		self.dealer_points = self.totalHandPoints(self.dealer_hand)

		while (sum((i > 16 and i < 22) for i in self.dealer_points) < 1 and sum(i > 21 for i in self.dealer_points) != len(self.dealer_points)):
			self.dealer_hand.append(self.drawCard())
			self.dealer_points = self.totalHandPoints(self.dealer_hand)

		return
	
	def switchForSplitHand(self):
		temp = copy.copy(self.hand)
		self.hand = copy.copy(self.split_hand)
		self.split_hand = temp
		
		self.points = self.totalHandPoints(self.hand)
		self.split_points = self.totalHandPoints(self.split_hand)
		
		self.split_movein = copy.copy(self.movein)
		self.movein = ['split']
		
		self.split_done = True

	def hit(self):
		node = self.spawn()
		node.hand.append(self.drawCard())
		
		node.points = self.totalHandPoints(node.hand)
		node.level = self.level + 1

		node.movein.append('hit')
		node.moves = node.possible_moves()

		self.children.append(node)

		return node

	def stand(self):
		node = self.spawn()
		node.points = self.totalHandPoints(self.hand)
		node.level = self.level + 1
		
		node.movein.append('stand')
		
		if not self.split_done and len(self.split_hand) > 0:
			node.switchForSplitHand()
		
		node.moves = node.possible_moves()
		
		self.children.append(node)
		
		return node
	
	def double_down(self):
		node = self.spawn()
		node.hand.append(self.drawCard())
		
		node.points = self.totalHandPoints(node.hand)
		node.level = self.level + 1

		node.movein.append('double_down')

		if (not self.split_done and len(self.split_hand) > 0):
			node.switchForSplitHand()
	
		node.moves = node.possible_moves()

		self.children.append(node)

		return node
	
	def split(self):
		node = self.spawn()
		node.hand = [self.hand[0], node.drawCard()]

		node.split_hand = [self.hand[1], node.drawCard()]
		
		node.points = self.totalHandPoints(node.hand)
		node.split_points = self.totalHandPoints(node.split_hand)
		node.level = self.level + 1

		node.movein.append('split')
		node.moves = node.possible_moves()
		
		self.children.append(node)

		return node
	
	def setmoves(self):
		return

	def make_move(self, move):
		moveDict = {'hit': self.hit, 'stand': self.stand, 'split': self.split, 'double_down': self.double_down}
		
		return moveDict[move]();
	
	def push_move(self, move):
		child = self.make_move(move)
		
		if type(child) == type([]):
			return child[0]
		
		return child

	def possible_moves(self):
		if (all(p > 20 for p in self.points)) or 'stand' in self.movein or 'double_down' in self.movein:
			return []

		possible_moves = ['hit', 'stand']
		
		if (len(self.movein) == 0) or (len(self.movein) == 1 and self.movein[0] == 'split'):
			possible_moves.append('double_down')

		if (len(self.hand) == 2) and (self.hand[0].value == self.hand[1].value) and (len(self.movein) == 0):
			possible_moves.append('split')

		return possible_moves

	def win(self):
		if not self.split_done:
			return 0 if self.tie(self.points, self.dealer_points) == True else self.winScore(self.hand, self.points, self.movein, self.dealer_points)
		else:
			return (0 if self.tie(self.points, self.dealer_points) == True else self.winScore(self.hand, self.points, self.movein, self.dealer_points)) + (0 if self.tie(self.split_points, self.dealer_points) == True else self.winScore(self.split_hand, self.split_points, self.split_movein, self.dealer_points))
		
	def winScore(self, player_hand, player_points, movein, dealer_points):
		score = ('double_down' in movein) + 1
		
		player_points = max([0] + [x for x in player_points if x < 22])

		if player_points == 0:
			return score * -1

		dealer_points = max([0] + [y for y in dealer_points if y < 22])

		if player_points > dealer_points and (dealer_points > 16 or dealer_points == 0):
			return score
		
		return score * -1

	def dealerWin(self):
		player_points = max([0] + [x for x in self.points if x < 22])

		if player_points == 0:
			return True

		dealer_points = max([0] + [y for y in self.dealer_points if y < 22])

		if dealer_points > 0 and dealer_points > player_points and dealer_points > 16:
			return True

		return False

	def tie(self, player_points, dealer_points):
		player_points = max([0] + [x for x in player_points if x < 22])

		if player_points == 0:
			return False

		dealer_points = max([0] + [y for y in dealer_points if y < 22])
		
		if dealer_points > 0 and dealer_points == player_points and dealer_points > 16:
			return True

		return False
