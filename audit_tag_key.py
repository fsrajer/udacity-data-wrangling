import re
import utils

def audit_tag_key(tag):
	"""
	Check for problematic characters and 
    split key if it has structure abc:def 
		-> set 'type' to abc and 'key' to def
	"""
	
	key = tag['key']
	errs = []
	if re.search(utils.problemchars, key):
		tag = None
		errs.append(('problematic characters in key', re.search(utils.problemchars, key).group(0)))
	
	elif re.match(utils.word_colon_word, key):
		sep = key.index(':')
		tag['type'] = key[:sep]
		tag['key'] = key[sep+1:]
	
	return tag, errs