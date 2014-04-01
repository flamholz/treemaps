#!/usr/bin/python

import argparse
import json

from hierarchy import HierarchyItem


def consume_line(l, current_parent):
    l_depth = int(l.count('\t'))
    l_name = l.strip()
    
    if l_depth == current_parent.depth:
        child = HierarchyItem(l_name, l_depth, current_parent)
        current_parent.add_child(child)
        return current_parent
    elif l_depth == current_parent.depth + 1:
        child = HierarchyItem(l_name, l_depth, current_parent)
        current_parent.add_child(child)
        return child
    else:
        grandparent = current_parent.parent
        new_parent = HierarchyItem(l_name, l_depth, grandparent)
        grandparent.add_child(new_parent)
        return new_parent


def Main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('hierarchy_filename',
                        help='Location of hierarchy file.')
    parser.add_argument('output_filename',
                        help='Where to output data to.')
    args = parser.parse_args()
    
    root = None
    current_parent = None
    print 'Parsing input'
    with open(args.hierarchy_filename) as f:
        for line in f:
            if current_parent is None:
                root = HierarchyItem.make_root(line.strip())
                current_parent = root
            else:
                current_parent = consume_line(line, current_parent)
    
    print 'Writing JSON'
    with open(args.output_filename, 'w') as out_f:
        d = root.as_dict()
        json.dump(d, out_f, indent=2)
    
    print 'Done'


if __name__ == '__main__':
    Main()
    