# -*- coding: utf-8 -*-

import sys
from base import *
from functions import *

def create_wrapper(x):
	args = x
	if len(x) > 2:
		args = x[:2]
		args.append(' '.join(x[2:]))
	return create(*args)

def roll_wrapper(x):
	if len(x) > 1:
		return roll(x[0], x[1])
	return roll(x[0])

def latest_wrapper(x):
	return latest(x[0])

functions = {"create": create_wrapper,
			 "roll": roll_wrapper,
			 "latest": latest_wrapper}

if __name__ == "__main__":
	while True:
		a = raw_input('>> ').split()
		try:
			print functions[a[0]](a[1:])
		except:
			print sys.exc_info()[1]