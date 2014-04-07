#!/usr/bin/python


class HierarchyItem(object):
    def __init__(self, name, depth, parent, color=None):
        self.name = name
        self.children = []
        self.parent = parent
        self.depth = depth
        self.size = None
        self.color = color
        
    @staticmethod
    def make_root(name):
        return HierarchyItem(name, 0, None)
    
    @staticmethod
    def _from_dict(d, parent):
        item_depth = 1
        if parent:
            item_depth = parent.depth + 1
            
        item = HierarchyItem(d['name'], item_depth, parent,
                             color=d.get('color'))
        children = [HierarchyItem._from_dict(cd, item)
                    for cd in d.get('children', [])]
        item.children = children
        return item
    
    @staticmethod
    def from_dict(d):
        return HierarchyItem._from_dict(d, None)
    
    def add_child(self, child):
        self.children.append(child)
    
    def empty(self):
        return not self.size and not self.children
    
    def prune(self):
        """Removes empty children recursively."""
        self.children = [c for c in self.children
                         if not c.empty()]
        for c in self.children:
            c.prune()
        
    def get_size(self):
        if self.children:
            return sum([c.get_size() for c in self.children])
        return self.size or 0
    
    def as_dict(self):
        d = {'name': self.name,
             'size': self.get_size(),
             'color': self.color}
        if self.children:
            d['children'] = [c.as_dict() for c in self.children]
        return d
