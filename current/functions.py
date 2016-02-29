types = {"deck": Deck, "dice": Dice, "pool": Pool}

def create(type, name, content):
	try:
		return types[type](name, content)
	except KeyError:
		raise InvalidTypeException("Invalid type for create command, expected {}, got {}."
			.format(', '.join(types), name))

def roll(name, count):
	try:
		return created[name].roll()
	except KeyError:
		raise InvalidTypeException("Entity with name {} is not created."
			.format(name))