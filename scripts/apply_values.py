#!/usr/bin/python

import argparse
import csv
import json

from hierarchy import HierarchyItem


def apply_values(item, value_mapping, name_mapping):
    if not item.children:
        item.size = value_mapping.get(item.name, 0.0)
    else:
        for child in item.children:
            apply_values(child, value_mapping, name_mapping)
    
    if item.name in name_mapping:
        item.name = name_mapping.get(item.name)


def Main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('hierarchy_filename',
                        help='Location of JSON hierarchy file.')
    parser.add_argument('values_filename',
                        help='Location of file containing per-key values.')
    parser.add_argument('mapping_filename',
                        help='Where to output data to.')
    parser.add_argument('output_filename',
                        help='Where to output data to.')
    args = parser.parse_args()
    
    print 'Loading hierarchy'
    with open(args.hierarchy_filename) as hf:
        hierarchy = json.load(hf)
        hierarchy = HierarchyItem.from_dict(hierarchy)
    
    print 'Loading name mapping'
    with open(args.mapping_filename) as mf:
        reader = csv.reader(mf, delimiter='\t')
        get_name = lambda v: v.split(':')[1]
        get_readable_name = lambda v: v.split(':')[0]
        base_mapping = list(reader)
        names_for_values = dict((get_name(v), k) for k, v in base_mapping)
        readable_name_mapping = dict((k, get_readable_name(v)) for k, v in base_mapping)
    
    print 'Loading values'
    with open(args.values_filename) as vf:
        reader = csv.reader(vf, delimiter='\t')
        values_mapping = dict((names_for_values[k], float(v)) for k, v in reader)

    print 'Applying values'
    apply_values(hierarchy, values_mapping, readable_name_mapping)
    with open(args.output_filename, 'w') as out_f:
        d = hierarchy.as_dict()
        json.dump(d, out_f, indent=2)   
    print 'Done'

if __name__ == '__main__':
    Main()
    