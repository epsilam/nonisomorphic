import srclib as lib
from numpy import sqrt
from itertools import permutations

class Graph:
    '''
    This class is instantiated with the binary list representation for each graph. 
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

def allGraphs(v,e):
    binlength = int((v+1)*v/2 + e - 1)
    binsum    = int((v+1)*v/2 - 1)
    graphList = []
    for binlist in lib.binarySequences(binlength, binsum):
        graph = Graph(binlist)
        graphList += [graph]
    return graphList

#Generate list of all graphs of v vertices and e edges which are non-isomorphic to eachother.
@lib.timer
def nonIsomorphicGraphs(v, e):
    graphs = allGraphs(v,e)
    isoClasses = [graphs[0].graphPermutations()]
    # for each G1 in graphs, check that it is not equal to any permutation of any graph in the list. If not, then add it.
    # For each G1, you need to ensure that if G1 is never in G2 for every G2, then G1 gets added to the list.
    for G1 in graphs:
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
    # Issue: for some reason all the elements in allGraphs seem to be nonIsomorphic

## HUGE OPTIMIZATION
# Keep the permutations of the graphs in the non-isomorphic graph list. Therefore whenever you want to check if a new graph is isomorphic to any of the graphs in the list, you don't have to generate new permutations. You just have to check if the graph is equal to any of the permutations of the already checked non-isomorphic graphs.

# This will require more memory but MUCH less time, because you are only generating new permutations when the graph is actually found to be nonisomorphic to each graph in the list.

# In this case, the list of non-isomorphic graphs can instead be a list of sublists, where each sublist contains all the permutations of one graph. This makes it easier to sequentially check through all the permutations. These 'sublists' can also be generators.

## NEXT OPTIMIZATION:
#CHECK LOOPS
#ALSO CHECK THAT SORTING THE TWO REDUCED LISTS RESULTS IN THE SAME THING
