#!/usr/bin/python


class HierarchyItem(object):
    def __init__(self, name, depth, parent):
        self.name = name
        self.children = []
        self.parent = parent
        self.depth = depth
        self.size = None
        
    @staticmethod
    def make_root(name):
        return HierarchyItem(name, 0, None)
    
    @staticmethod
    def _from_dict_depth(d, depth, parent):
        item = HierarchyItem(d['name'], depth, parent)
        children = [HierarchyItem._from_dict_depth(cd, depth+1, item)
                    for cd in d.get('children', [])]
        item.children = children
        return item
    
    @staticmethod
    def from_dict(d):
        return HierarchyItem._from_dict_depth(d, 0, None)
    
    def add_child(self, child):
        self.children.append(child)
        
    def get_size(self):
        if self.children:
            return sum([c.get_size() for c in self.children])
        return self.size or 0
    
    def as_dict(self):
        d = {'name': self.name,
             'depth': self.depth,
             'size': self.get_size()}
        if self.children:
            d['children'] = [c.as_dict() for c in self.children]
        return d
