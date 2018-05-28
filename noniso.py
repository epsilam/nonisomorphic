import srclib as lib
from numpy import sqrt
from itertools import permutations

class Graph:
    '''
    This class is instantiated with the binary list representation for each graph. A graph is identified by its reduced list representation, denoted self.reduced. This is basically the lower triangle of its adjacency matrix squashed into one list, while the binary list representation is the reduced list expanded into stars-and-bars notation to make it easier to generate all graphs, as we can more efficiently generate all lists of arbitrary length containing an arbitrary number of 1s. 
    '''

    def __init__(self, binlist):
        #=== Store the binary representation
        self.binaryRep = binlist
        
        #=== Determine reduced list representation
        reducedList = []
        counter = 0
        sequence = self.binaryRep + [1] #Since it counts 0s before each 1, we need to make sure there is a 1 at the end so that the last couple of 0s are counted.
        for digit in sequence:
            if digit == 0:
                counter += 1
            elif digit == 1:
                reducedList = reducedList + [counter]
                counter = 0
        self.reduced = reducedList

        #=== Find number of edges and vertices
        # number of edges
        self.size  = sum(self.reduced)
        # number of vertices
        self.order = int((sqrt(1+8*len(self.reduced)) - 1)/2)
    
    def prettyprint(self):
        matrix = []
        for i in range(self.order):
            matrix += [self.reduced[int((i+1)*i/2):int((i+2)*(i+1)/2)]]
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))

    #Permute a graph's reduced list according to a given permutation of its vertices.
    def permute(self, permutation):
        indexedReducedList = {}
        countX = 0
        countY = 0
        for entry in self.reduced:
            indexedReducedList[(countX, countY)] = entry
            if countY < countX:
                countY += 1
            elif countY == countX:
                countX += 1
                countY = 0
        permutedIndexedReducedList = {}
        for index in indexedReducedList:
            x = permutation[index[0]]
            y = permutation[index[1]]
            permutedIndexedReducedList[(x,y)] = indexedReducedList[index]
        for index in permutedIndexedReducedList:
            if index[0] < index[1]:
                permutedIndexedReducedList[(index[1],index[0])] = permutedIndexedReducedList[index]
                del permutedIndexedReducedList[index]
        permutedReducedList = []
        for index in sorted(permutedIndexedReducedList):
            permutedReducedList += [permutedIndexedReducedList[index]]
        return permutedReducedList

    # Generate all permutations of vertices of this graph (i.e., all graphs in reduced list form which are isomorphic to self)
    def graphPermutations(self):
        ps = []
        for p in permutations(range(self.order)):
           ps += [self.permute(p)]
        return ps
    
    def isomorphic(self, other):
        pass

#Generate list of all labeled graphs with v vertices and e edges. (Note: generates ALL graphs, not those different up to isomorphism.)
def allGraphs(v,e):
    binlength = int((v+1)*v/2 + e - 1)
    binsum    = int((v+1)*v/2 - 1)
    graphList = []
    for binlist in lib.binarySequences(binlength, binsum):
        graph = Graph(binlist)
        graphList += [graph]
    return graphList

#Generate list of all different undirected graphs (including multigraphs) of v vertices and e edges up to isomorphism.
@lib.timer
def nonIsomorphicGraphs(v, e):
    graphs = allGraphs(v,e)
    isoClasses = [graphs[0].graphPermutations()] #isoClasses contains permutations of each graph. All permutations of one graph are isomorphic to eachother, therefore isoClasses really contains each isomorphism class.
    for G1 in graphs: # for each G1 in graphs, check that it is not equal to any permutation of any graph in the isoClasses. If not, then add it.
        breakVar = False
        for G2 in isoClasses:
            if G1.reduced in G2:
                # set breakVar to True if isomorphism detected
                breakVar = True
                break
        if breakVar == True:
            continue
        else:
            isoClasses += [G1.graphPermutations()]
            print(G1.reduced)
            G1.prettyprint()
            print("\n")
    print(len(isoClasses), "non-isomorphic graphs")

## NEXT OPTIMIZATION:
#If it doesn't take too much more time, it is possible to sort out the graph you are comparing and check that the numbers of edges between vertices match up. (e.g., if a graph G1 has a pair of vertices with 5 edges between then but another graph G2 has no pairs of vertices with 5 edges between them, then G1 and G2 are definitely not isomorphic. You can check this by sorting the reduced lists and making sure they are equal. If they are, then you can continue checking to see if the graph is equal to any of the (unsorted) permutations of the other graph.)
