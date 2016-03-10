# -*- coding: utf-8 -*-

from base import *
import re

types = {"deck": Deck, "dice": Dice, "pool": Pool}

class InvalidTypeException(Exception):
    def __init__(self, value):
        self.value = "Entity with name {} is not created.".format(value)
    def __str__(self):
        return repr(self.value)

class InvalidNameException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

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
		return c
	except KeyError:
		raise InvalidTypeException("Invalid type for create command, expected {}, got {}."
			.format(', '.join(types), name))

def roll(name, count = None):
	if count == None:
		count = 1
	try:
		int(name)
		return name
	except:
		if '+' in name:
			name = name.split('+')
			r = ''
			for x in range(1, int(count)+1):
				r += str(x) + ":\n"
				for member in name:
					r += "\t{}: {}".format(member, roll(member))
					r += "\n"
			return r
		else:
			try:
				return get_entity(name).roll(int(count))
			except KeyError:
				raise InvalidNameException(name)