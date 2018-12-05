

def reverse_tuple_lookup(k, t):
	d = {}
	for g in t:
		d[g[1]] = g[0]
	v = d.get(k, '')
	return v

def get_choice_string(c, k):
	for items in c:
		if str(k) == str(items[0]):
			return items[1]
	
	return k