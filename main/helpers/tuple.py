

def reverse_tuple_lookup(k, t):
	d = {}
	for g in t:
		d[g[1]] = g[0]
	v = d.get(k, '')
	return v
