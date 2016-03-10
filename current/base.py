# -*- coding: utf-8 -*-

import random, re

class InvalidTypeException(Exception):
    def __init__(self, value):
        self.value = "Invalid type for create command, expected {}, got {}.".format(', '.join(types), value)
    def __str__(self):
        return repr(self.value)

class InvalidNameException(Exception):
    def __init__(self, value):
        self.value = "Entity with name {} is not created.".format(value)
    def __str__(self):
        return repr(self.value)


created = {}

class Dice(object):
	def __init__(self, name, args):
		if args == []:
			self.vals = dices["Default"]
		elif len(args) == 1:
			try:
				self.vals = dices[args[0]]
			except:
				self.vals = map(str, range(1, int(args[0])+1))
		else:
			self.vals = args
		self.name = name
		self.latest = None

	def roll(self, *options):
		options = tuple(options)

		choice = []
		mod = 0

		if options == ():
			count = 1
		else:
			count = options[0]

		for x in range(count):
			choice += random.choice(self.vals)

		self.latest = choice[-1]
		
		if len(choice) == 1:
			return choice[0]
		
		return choice

class Deck(object):
	def __init__(self, name, *args):
		if args == ():
			self._vals = decks["Default"]
		else:
			try:
				self._vals = tuple(decks[args[0]])
			except:
				self._vals = tuple(args)
		self.shuffle()
		self.name = name
		self.latest = None

	def roll(self, count = None):
		choice = []
		if count == None:
			count = 1

		for x in range(1, count+1):
			try:
				t = random.choice(self.vals)
				self.latest = t
			except:
				msg = "The deck {0} is empty. Type \"shuffle {0}\" to shuffle deck.".format(self.name)
				if choice != '':
					msg = choice+'\n'+msg
				return msg
			choice.append(t)
			self.vals.remove(t)

		if len(choice) == 1:
			choice = choice[0]

		return choice

	def shuffle(self):
		self.vals = list(self._vals)

class Pool(object):
	def __init__(self, name, content):
		self.content = [x for x in content.split() if x != name]
		self.name = name

	def roll(self, count = None):
		if count == None:
			count = 1
		choice = []
		return roll('+'.join(self.content), count)

decks = {
		 "Default": ('1 spades', '1 clubs', '1 hearts', '1 diamonds',
		 			 '2 spades', '2 clubs', '2 hearts', '2 diamonds',
		 			 '3 spades', '3 clubs', '3 hearts', '3 diamonds', 
		 			 '4 spades', '4 clubs', '4 hearts', '4 diamonds', 
		 			 '5 spades', '5 clubs', '5 hearts', '5 diamonds', 
		 			 '6 spades', '6 clubs', '6 hearts', '6 diamonds', 
		 			 '7 spades', '7 clubs', '7 hearts', '7 diamonds', 
		 			 '8 spades', '8 clubs', '8 hearts', '8 diamonds', 
		 			 '9 spades', '9 clubs', '9 hearts', '9 diamonds', 
		 			 '10 spades', '10 clubs', '10 hearts', '10 diamonds', 
		 			 'J spades', 'J clubs', 'J hearts', 'J diamonds', 
		 			 'Q spades', 'Q clubs', 'Q hearts', 'Q diamonds', 
		 			 'K spades', 'K clubs', 'K hearts', 'K diamonds', 
		 			 'A spades', 'A clubs', 'A hearts', 'A diamonds'),
		 "IFutark": ("Fehu: благополучие", "Uruz: дикий бык", "Thurs: враг", "Ansuz: бог, судьба",
		 			"Raidho: путешествие", "Kenaz: болезнь", "Gebo: подарок", "Wunjo: удача, счастье",
		 		    "Hagal: град, разрушение", "Nauthiz: нужда, рабство", "Isa: лед", "Jera: годы, урожай", 
		 		    "Iwar: тис, защита", "Perth: отдых", "Algiz: лось", "Sowlo: солнце",
		 		    "Theiwaz: Тюр", "Berkana: береза", "Eihwaz: лошадь", "Mannaz: мужчина, человек", 
		 		    "Laguz: вода", "Inguz: плодородие", "Dagaz: день", "Odal: дом, одаль", "Odin: неопределенность"),
		 "Futark": ("Fehu", "Ur", "Thurs", "Ansuz", "Raidho", "Kenaz", "Gebo", "Wunjo",
		 		    "Hagal", "Naudiz", "Isa", "Jara", "Iwar", "Perth", "Algiz", "Sowlo",
		 		    "Theiwaz", "Berkana", "Eihwaz", "Mannaz", "Laguz", "Inguz", "Dagaz", "Odal", "Odin")
		}

dices = {"Default": ('1', '2', '3', '4', '5', '6')}

types = {"deck": Deck, "dice": Dice, "pool": Pool}

def get_entity(name):
	pat = re.compile(r"^d[0-9]+$")
	if pat.match(name):
		return Dice(name, name.split('d')[1])
	else:
		try:
			return created[name]
		except:
			raise InvalidNameException(name)

def set_entity(name, val):
	created[name] = val

def create(type, name, *args):
	try:
		c = types[type](name, *args)
		set_entity(name, c)
		return "{} {} sucessfully created\n".format(type, name)
	except KeyError:
		raise InvalidTypeException(type)

def roll(name, count = None):
	if count == None:
		count = 1
	count = int(count)
	try:
		int(name)
		return name
	except:
		if '+' in name:
			i = 0
			name = name.split('+')
			r = []
			for x in range(1, int(count)+1):
				r.append({})
				for member in name:
					r[-1][member+":"+str(i)] = roll(member)
					i += 1
			return m_print(r)
		else:
			try:
				return get_entity(name).roll(int(count))
			except KeyError:
				raise InvalidNameException(name)

def latest(name):
	return m_print(get_entity(name).latest)

def m_print(data):
	r = ''
	if type(data) == type(int()) or type(data) == type(str()):
		r = str(data)

	elif type(data) == type(list()):
		for i, e in enumerate(data):
			r += "{}: {}\n".format(i+1, m_print(e))

	elif type(data) == type(dict()):
		for i in data:
			r += "\t{}: {}\n".format(i[:i.index(":")], m_print(data[i]))

	return r