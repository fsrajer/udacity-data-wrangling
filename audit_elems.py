from audit_fields import audit_fields, node_fields, tag_fields, way_fields, way_nodes_fields
from audit_tag_key import audit_tag_key 
from audit_postcode import audit_postcode 
from audit_streetname import audit_streetname 
from audit_country import audit_country 
from audit_house_ids import audit_housenumber, audit_house_id, has_some_house_id
from audit_location import audit_location

def audit_tags(elem):
    tags = []
    errs = []
    for tag in elem.iter('tag'):
        parsed, errs_curr = audit_fields(tag, tag_fields)
        if parsed:
            parsed['id'] = int(elem.get('id'))
            parsed['type'] = 'regular'
            parsed, errs_curr = audit_tag_key(parsed)
        
        if parsed and parsed['type'] == 'addr':
            if parsed['key'] == 'postcode':
                parsed, errs_curr = audit_postcode(parsed)
            elif parsed['key'] == 'street':
                parsed, errs_curr = audit_streetname(parsed)
            elif parsed['key'] == 'country':
                errs_curr = audit_country(parsed)
            elif parsed['key'] == 'housenumber':
                parsed = audit_housenumber(parsed)
        
        if errs_curr:
            errs.append(('ignored tag', tag.attrib, errs_curr))
        if parsed:
            tags.append(parsed)
    
    if errs:
        errs = [(errs, tags)]
    
    if has_some_house_id(tags):
        tags, errs_curr = audit_house_id(tags)
        if errs_curr:
            errs.append(errs_curr)
    
    return tags, errs

def audit_node(node):
    parsed, errs = audit_fields(node, node_fields)
            
    if parsed:
        parsed, errs_loc = audit_location(parsed)
        tags, errs_tags = audit_tags(node)
        errs = errs_loc + errs_tags
        
    if not parsed:
        tags = None
            
    return parsed, tags, errs
	
def audit_way_nodes(way):
    nodes = []
    errs = []
    position = 0
    for node in way.iter('nd'):
        parsed, errs_curr = audit_fields(node, way_nodes_fields) 
        
        if parsed:
            parsed['id'] = int(way.get('id'))
            parsed['position'] = position
            nodes.append(parsed)
            position += 1
            
        else:
            errs.append('Bad way node', node.attrib, errs_curr)
    
    return nodes, errs
	
def audit_way(way):
    
    parsed, errs = audit_fields(way, way_fields)
            
    if parsed:
        nodes, errs_nodes = audit_way_nodes(way)
        tags, errs_tags = audit_tags(way)
        errs = errs_nodes + errs_tags
    
    if not parsed:
        nodes = None
        tags = None
        
    return parsed, nodes, tags, errs