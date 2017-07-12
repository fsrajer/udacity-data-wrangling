import re

def audit_housenumber(tag):
    tag['value'] = tag['value'].replace('ev. ','ev.')
    return tag
	
# Patterns for checking all types of house ids in the Czech system
pattern_conscription = r'[1-9]+?[0-9]*'
pattern_street = r'[1-9]+?[0-9]*[a-zA-Z]?'
pattern_provisional = r'[1-9]+?[0-9]*'
patterns_house_id = \
            {'conscription': re.compile(r'^' + pattern_conscription + '$'), # popisne
            'street': re.compile(r'^' + pattern_street + '$'), # orientacni
            'provisional': re.compile(r'^' + pattern_provisional + '$'), # evidencni
            'house': re.compile(r'^' + \
                    '(ev\.' + pattern_provisional + ')|(' + pattern_conscription + ')' \
                        + '(/' + pattern_street + ')?$')} # ((ev.)evidencni)|(popisne)(/orientacni)?

def has_some_house_id(tags):
	"""Does it have at least one id?"""
	
	for tag in tags:
		if tag['key'][:-6] in patterns_house_id:
			return True
	return False

def get_house_ids(tags):
	"""Get all the ids from all the tags"""
    
	house_id = {}
	for tag in tags:
		id_type = tag['key'][:-6]
        
        if id_type in patterns_house_id: 
            house_id[id_type] = tag['value']
            
	return house_id
	
def audit_house_id(tags):
    """
    Verify that all house id tags are consistent and try to
    fill in the missing ones if they can be inferred.
    If there is some inconsistency, tags will be returned
    in their original format and the second return value will
    be error info.
    """

    house_id = get_house_ids(tags)
    errs = []
    
    # check that the patterns are correct
    for id_type, id_value in house_id.items():
        
        match = re.match(patterns_house_id[id_type], id_value)
        
        # unusual format, maybe that house is a street number only
        if id_type == 'house':
                
            # this handles a few cases which are in the database
            if id_value[0] == '?':
                id_value = id_value[1:]
            if id_value[0] == '/':
                id_value = id_value[1:]
                    
            # either nothing else is known, so test street pattern
            # or street is known so test equality
            if (len(house_id) == 1 and not match and re.match(patterns_house_id['street'], id_value))                     or ('street' in house_id and house_id['street'] == id_value): 
                
                # keep only street tag - house will be composed correctly later
                house_id['street'] = id_value
                del house_id['house']
                tags = [tag for tag in tags if tag['key'] != 'housenumber']
                match = True 
        
        if not match:
            errs.append((id_type + ' does not match pattern', id_value))
    
    if errs:
        return tags, [('House id pattern not matching', errs, tags)]
    
    if 'provisional' in house_id and 'conscription' in house_id:
        errs.append(('We cannot have both provisional and conscription', house_id))    
    
    # house unknown, use other fields to compose it
    elif 'house' not in house_id:
        housenumber = ''
        if 'conscription' in house_id:
            housenumber = house_id['conscription']
        elif 'provisional' in house_id:
            housenumber = 'ev.' + house_id['provisional']
        
        if 'street' in house_id:
            housenumber = housenumber + '/' + house_id['street']
        
        if housenumber != '':
            tags.append({'id': tags[0]['id'], # all tags have parent's id
                    'key': 'housenumber',
                    'value': housenumber,
                    'type': 'addr'})
    
    # use house to check or fill in other fields 
    else:
        is_provisional = house_id['house'][:3] == 'ev.'
        if is_provisional:
            house_id['house'] = house_id['house'][3:]
            first_name = 'provisional'
        elif house_id['house'][0] == '/':
            first_name = ''
        else:
            first_name = 'conscription'
            
        sep = house_id['house'].find('/')
        has_street = sep >= 0
        
        first = house_id['house']
        if has_street:
            second = first[sep+1:]
            first = first[:sep]
            
        if first_name in house_id:
            if first != house_id[first_name]:
                errs.append(('First number is not consistent', house_id))
        elif first != '' and first_name != '':
            tags.append({'id': tags[0]['id'], # all tags have parent's id
                    'key': first_name + 'number',
                    'value': first,
                    'type': 'addr'})
            
        if has_street:
            if 'street' in house_id:
                if second != house_id['street']:
                    errs.append(('Street number is not consistent', house_id))
            else:
                tags.append({'id': tags[0]['id'], # all tags have parent's id
                        'key': 'streetnumber',
                        'value': second,
                        'type': 'addr'})
        
    return tags, errs   