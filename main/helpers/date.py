
def isYear(_y):
	"""
	This methods verifies if given string is Nepali year or not
	:params : string _y
	:returns : True | False
	"""
	try:
		_y = int(_y)
	except:
		return False
	if len(_y) != 4:
		return False

	if _y[0] not in [2,3]:
		return False

	return True