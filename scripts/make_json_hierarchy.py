#!/usr/bin/python

import argparse
import csv
import json

from hierarchy import HierarchyItem


def consume_line(l, previous_item):
    l_depth = int(l.count('\t'))
    l_name = l.strip()
    
    if l_depth == previous_item.depth:
        # same depth as previous - child of same parent
        parent = previous_item.parent
        new_item = HierarchyItem(l_name, l_depth, parent)
        parent.add_child(new_item)
        return new_item
    elif l_depth == previous_item.depth + 1:
        # depth one higher - child of previous item
        parent = previous_item
        child = HierarchyItem(l_name, l_depth, parent)
        parent.add_child(child)
        return child
    else:
        # lower depth - child of some ancestor
        depth_change = previous_item.depth - l_depth
        assert depth_change > 0
        
        appropriate_parent = previous_item.parent
        for _ in xrange(depth_change):
            appropriate_parent = appropriate_parent.parent

        new_item = HierarchyItem(l_name, l_depth, appropriate_parent)
        appropriate_parent.add_child(new_item)
        return new_item


def Main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('hierarchy_filename',
                        help='Location of hierarchy file.')
    parser.add_argument('output_filename',
                        help='Where to output data to.')
    parser.add_argument('-c', '--color_filename',
                        help='Name of the color mapping file.')
    args = parser.parse_args()
    
    color_map = dict()
    if args.color_filename:
        with open(args.color_filename) as f:
            for line in csv.reader(f, delimiter='\t'):
                id, r, g, b = line
                id = id.strip()
                assert id not in color_map, "duplicate ID"
                r, g, b = 255 * float(r), 255 * float(g), 255 * float(b)
                hexval = 'rgb(%d, %d, %d)' % (r, g, b)
                color_map[id] = hexval
    
    root = None
    current_item = None
    print 'Parsing input'
    with open(args.hierarchy_filename) as f:
        for line in f:
            if current_item is None:
                root = HierarchyItem.make_root(line.strip())
                current_item = root
            else:
                current_item = consume_line(line, current_item)
            if current_item.name in color_map:
                current_item.color = color_map[current_item.name]
    
    
    print 'Writing JSON'
    with open(args.output_filename, 'w') as out_f:
        d = root.as_dict()
        json.dump(d, out_f, indent=2)
    
    print 'Done'


if __name__ == '__main__':
    Main()
    