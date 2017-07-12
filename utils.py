import xml.etree.cElementTree as ET
import re
import pprint
from collections import defaultdict

word_colon_word = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\, \t\r\n]') # we allow for a dot as opposed to the case-study code

def ensure_type(str_value, expected_type):
    """Returns parsed type or None if not possible"""
    
    # avoids converting strings to strings - so it doesn't have to handle non-ascii chars
    if expected_type == type(str()):
        return str_value
    
    try:
        return expected_type(str_value)
    except:
        return None
    
# My pprint class which handles utf8
# source:
# https://stackoverflow.com/questions/10883399/unable-to-encode-decode-pprint-output
class PrettyPrinterUTF8(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()
			
def categorize_errs(errs):
	"""
	Given the errs as used in the main auditing script,
	create a dictionary, where the key is the main errror message
	and value is a list of errors with the same message
	"""
	
	errs_cat = defaultdict(list)
	for err in errs:
		try:
			cat = err[2][0][0][0]
			errs_cat[cat].append(err)
		except:
			errs_cat['other'].append(err)
	return errs_cat