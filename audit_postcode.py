import re 

pattern_postcode_alternative = re.compile(r'^[0-9]{3} [0-9]{2}$')

def audit_postcode(tag):
	"""
	Check bounds of the postcode.
	Prague region included fully, Central Bohemian and Usti nad Labem regions partially.
	"""
	
	errs = []
	try:
		if re.match(pattern_postcode_alternative, tag['value']):
			tag['value'] = tag['value'].replace(' ', '')
		postcode = int(tag['value'])
		if not (10000 <= postcode <= 29599 or 40000 <= postcode <= 44199):
			tag = None
			errs = ['postcode outside of valid range']
	except:
		tag = None
		errs = ['postcode not integer']
	return tag, errs