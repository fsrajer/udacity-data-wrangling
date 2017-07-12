import re
from collections import defaultdict

import utils
from audit_elems import audit_node, audit_way

#osm_filename = "prague_sample_k1000.osm"
osm_filename = "prague_sample_k500.osm"
#osm_filename = "prague_sample_k250.osm"
#osm_filename = "prague_sample_k100.osm"
#osm_filename = "prague_sample_k25.osm"
#osm_filename = "prague_czech-republic.osm"

pp = utils.PrettyPrinterUTF8()

errs = []
def audit(osm_filename):
    global errs
    
    count = 0
#    tag_count = defaultdict(int)
#    streets = defaultdict(int)
    errs = []
    for elem in utils.get_element(osm_filename, tags=('node', 'way')):
        
        count += 1  
        
        if elem.tag == "node":
            node, tags, errs_curr = audit_node(elem)
        elif elem.tag == "way":
            way, way_nodes, tags, errs_curr = audit_way(elem)
        
            
        if errs_curr:
            errs.append(('bad elem', elem.attrib, errs_curr))
#            pp.pprint(errs[-1])
#        else:
#            for tag in tags:
#                tag_count[tag['type'] + ":" + tag['key']] += 1
                
#                if tag['key'] == 'street' and len(tag['value'].split(' ')) > 1:
#                    words = tag['value'].split(' ')
#                    streets[words[0]] +=1
#                    streets[words[-1]] +=1
              
                 
#        if count > 1000:
#            break
    errs_glob = errs
    print("Num errors: {}".format(len(errs)))
    errs_cat = utils.categorize_errs(errs)
    for cat in errs_cat:
        print("{}: {}".format(cat, len(errs_cat[cat])))
#    for key in sorted(streets, key=streets.get, reverse=True):
#        if streets[key] == 1:
#            break
#        print(key + ": " + str(streets[key]))
#    print("")
#    for key in sorted(tag_count, key=tag_count.get, reverse=True):
#        print(key + ": " + str(tag_count[key]))
#        if tag_count[key] < 100:
#            break

audit(osm_filename)