import csv
import codecs
import cerberus

import utils
from audit_elems import audit_node, audit_way
from schema import db_schema

#osm_filename = "prague_sample_k1000.osm"
osm_filename = "prague_sample_k500.osm"
#osm_filename = "prague_sample_k250.osm"
#osm_filename = "prague_sample_k100.osm"
#osm_filename = "prague_sample_k25.osm"
#osm_filename = "prague_czech-republic.osm"

csv_filename_nodes = "nodes.csv"
csv_filename_nodes_tags = "nodes_tags.csv"
csv_filename_ways = "ways.csv"
csv_filename_ways_nodes = "ways_nodes.csv"
csv_filename_ways_tags = "ways_tags.csv"
csv_filename_users = "users.csv"

node_fields_csv_names = ['id', 'lat', 'lon', 'uid', 'version', 'changeset', 'timestamp']
way_fields_csv_names = ['id', 'uid', 'version', 'changeset', 'timestamp']
tag_fields_csv_names = ['id', 'key', 'value', 'type']
way_nodes_fields_csv_names = ['id', 'node_id', 'position']
user_fields_csv_names = ['id', 'username']

def validate_element(element, validator, schema=db_schema):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        pp.pprint(element)
        raise Exception(message_string.format(field, error_string))

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
    
    def write(self, rowrows):
        if type(rowrows) == type(list()):
            self.writerows(rowrows)
        elif type(rowrows) == type(dict()):
            self.writerow(rowrows)
        else:
            raise Exception("Wrong type to write, list or dict expected")

errs = []
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(csv_filename_nodes, 'wb') as nodes_file,          codecs.open(csv_filename_nodes_tags, 'wb') as nodes_tags_file,          codecs.open(csv_filename_ways, 'wb') as ways_file,          codecs.open(csv_filename_ways_nodes, 'wb') as ways_nodes_file,          codecs.open(csv_filename_ways_tags, 'wb') as ways_tags_file,          codecs.open(csv_filename_users, 'wb') as users_file:

        nodes_writer = UnicodeDictWriter(nodes_file, node_fields_csv_names)
        nodes_tags_writer = UnicodeDictWriter(nodes_tags_file, tag_fields_csv_names)
        ways_writer = UnicodeDictWriter(ways_file, way_fields_csv_names)
        ways_nodes_writer = UnicodeDictWriter(ways_nodes_file, way_nodes_fields_csv_names)
        ways_tags_writer = UnicodeDictWriter(ways_tags_file, tag_fields_csv_names)
        users_writer = UnicodeDictWriter(users_file, user_fields_csv_names)
        
        writers = {'nodes': nodes_writer,
                  'nodes_tags': nodes_tags_writer,
                  'ways': ways_writer,
                  'ways_nodes': ways_nodes_writer,
                  'ways_tags': ways_tags_writer,
                  'users': users_writer}
        
        # It seems that sqlite does not like headers
        #for writer in writers.values():
        #    writer.writeheader()
            
        validator = cerberus.Validator()
        errs = []
        user_ids = set()
    
        for elem in utils.get_element(file_in, tags=('node', 'way')):
            
            parsed = {}
            if elem.tag == "node":
                node, tags, errs_curr = audit_node(elem)
                if node:
                    parsed['nodes'] = node
                    parsed['nodes_tags'] = tags
                        
            elif elem.tag == "way":
                way, way_nodes, tags, errs_curr = audit_way(elem)
                if way:
                    parsed['ways'] = way 
                    parsed['ways_nodes'] = way_nodes
                    parsed['ways_tags'] = tags 
                    
            if errs_curr:
                errs.append(('bad elem', elem.attrib, errs_curr))
                #pp.pprint(errs[-1])
            
            if parsed:
                
                # move username to the users table
                uid = parsed[elem.tag + 's']['uid']
                username = parsed[elem.tag + 's']['user']
                del parsed[elem.tag + 's']['user']

                if uid not in user_ids:
                    user_ids.add(uid)
                    parsed['users'] = {'id': uid,
                                      'username': username}
                
                if validate is True:
                    validate_element(parsed, validator)
            
                for table in parsed:
                    writers[table].write(parsed[table])
                    
process_map(osm_filename, validate=True)