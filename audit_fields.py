from utils import ensure_type

# mappings for parsing .osm into python dictionary/csv
# structure of the following variables is (original_name, type, target_name)

node_fields_names = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
node_fields = zip(node_fields_names, \
                    map(type, [int(), float(), float(), str(), int(), int(), int(), str()]), \
                    node_fields_names)

way_fields_names = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
way_fields = zip(way_fields_names, \
                    map(type, [int(), str(), int(), int(), int(), str()]),
                    way_fields_names)

tag_fields = zip(['k', 'v'], \
                map(type, [str(), str()]), \
                ['key', 'value'])

way_nodes_fields = zip(['ref'], \
                       [type(int())], \
                       ['node_id'])
			
			
def audit_fields(elem, fields):
    """Parse any element into dictionary using the given fields"""
    errs = []
    parsed = {}
    for field, field_type, dict_field in fields:
        if field not in elem.attrib:
            errs.append(('missing value', field))
        else:
            value = ensure_type(elem.get(field), field_type)
            if not value:
                errs.append(('wrong type', field))
            else:
                parsed[dict_field] = value
    
    if errs:
        parsed = None
    return parsed, errs