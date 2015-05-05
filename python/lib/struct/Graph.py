"""
A module for doing things with graphs. Works great so far!
"""
import numpy

NO_EDGE = -1

class Node():
    def __init__(self, value=None):
        self.visited = False
        self.value = value
        self.edges = []
        
    def append(self,edge):
        self.edges.append(edge)
    def __iter__(self):
        """
        Iterate through the edges
        """
        for edge in self.edges:
            yield edge

class Edge():
    def __init__(self,src,dest,value):
        self.src = src
        self.dest = dest
        self.value = value

def Paths(nodes, head=None, tail=None):
    """
    Generate a list of paths from head to tail. If head or tail is None,
    it will iterate over all possible heads and tails, respectively. 
    
    It does not loop over pre-searched nodes 
    """
    paths = []
    if head == None:
        for node in nodes:
            _SubPaths(paths,node,tail=tail)
    else:
        _SubPaths(paths,head,tail=tail)
    return paths

def _SubPaths(paths, head, tail=None, path=[]):
    """
    Ignore this function (used by Paths)
    WHAT DOES THIS FUNCTION DO???
    """
    path.append(head)
    head.visited = True
    for edge in head:
        # Don't include visited nodes (no loops)
        if edge.dest.visited == True:
            continue
        if tail != None and edge.dest == tail:
            # Found the destination
            # Make a temporary list to append edge.dest to path, but don't
            # modify path
            a = path[:]
            a.append(edge.dest)
            paths.append(a)
            
            # There may be other ways to tail, so continue
            continue
        
        else:
            if tail == None:
                # This will get super huge
                # Make a temporary list to append edge.dest to path, but don't
                # modify path
                a = path[:]
                a.append(edge.dest)
                paths.append(a)
            _SubPaths(paths,edge.dest,tail=tail,path=path)
    # Remove head from end of list
    path.pop()
    head.visited = False

def InitGraphFromAdjacencyMatrix(edgeValues, nodes):
    """
    Parameters
    ----------
    edgeValues : 2D numpy array
        Values for each edge between node r(ow) and node c(olumn). 
        Edge value of NO_EDGE for no edge between the two nodes
    nodes : list of Node
        List of instances of Node in order
    """
    for r, row in enumerate(edgeValues):
        for c, value in enumerate(row):
            if value != NO_EDGE:
                nodes[r].edges.append(Edge(nodes[r],nodes[c],value))


        
if __name__ == '__main__':
    """
    Try an example of going from the first node to the last node.
    """
    n = 5
    edgeValues = numpy.ones((n,n))
    nodes = [Node(value=i) for i in range(n)]
    InitGraphFromAdjacencyMatrix(edgeValues, nodes)
    paths = Paths(nodes,head=nodes[0],tail=nodes[-1])
    for path in paths:
        string = ''
        for node in path:
            string += str(node.value) + ' '
        print string
    
    # This is a tricky one. Given n, how many paths should there be?
    #  n-2 * (((n-2)*(n-1))/2 - 1) ?
#     assert len(paths) == 1 + (n-2)**2
        
            
        