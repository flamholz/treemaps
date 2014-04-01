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
    
    def as_dict(self):
        d = {'name': self.name}
        if self.children:
            d['children'] = [c.as_dict() for c in self.children]
        else:
            d['size'] = self.size
        return d
