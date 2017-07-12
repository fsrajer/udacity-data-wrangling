def audit_location(node):
	"""Check bounds of latitude and longitude"""
    
	errs = []
	for bound, field in zip([90., 180.], ['lat', 'lon']):
		if not (-bound <= node[field] <= bound):
			errs.append(('invalid value', field, node))
			node = None
			break
	return node, errs