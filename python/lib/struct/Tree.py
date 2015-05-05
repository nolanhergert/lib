"""
Eventually move this into Graph.py. For now just prototyping with a
binary search tree
"""

class Node():
    def __init__(self, val, data):
        self.val = val
        self.data = data
    def __cmp__(self):
        return 
    
def Left(idx):
    return idx*2+1

def Right(idx):
    return (idx+1)*2

        

def Find(head, value):
    """
    Find a node in a binary tree based on its value
    
    Parameters
    ----------
    head : Node
        The current node we are parsing. On initialization, it's the head of
        the tree.
    value : <T>
        The value we are looking for. 
    """
    node = None
    
    
    
    
    return node

if __name__ == '__main__':
    head = Node()

