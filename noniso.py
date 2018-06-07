import srclib as lib
from numpy import sqrt
from itertools import permutations

class Graph:
    '''
    This class is initialized either with the binary list representation or the reduced list representation for each graph.
    If only a binary list representation is given, the reduced list is computed from it.
    Each graph is identified by its reduced list representation, denoted self.reduced.
    This is basically the lower triangle of its adjacency matrix squashed into one list,
    while the binary list representation is the reduced list expanded into stars-and-bars
    notation to make it easier to generate all graphs, as we can more efficiently
    generate all lists of arbitrary length containing an arbitrary number of 1s.
    '''

    def __init__(self, binlist=None, reduced=None):
        #=== Store the binary representation
        self.binlist = binlist

        #=== Determine reduced list representation
        if reduced == None and binlist != None:
            reducedList = []
            counter = 0
            sequence = self.binlist + [1] #Since it counts 0s before each 1, we need to make sure there is a 1 at the end so that the last couple of 0s are counted.
            for digit in sequence:
                if digit == 0:
                    counter += 1
                elif digit == 1:
                    reducedList = reducedList + [counter]
                    counter = 0
            self.reduced = reducedList
        # If user passed a value to reduced, then use this instead of calculating the reduced list. This was primarily used for debugging purposes.
        elif reduced != None:
            self.reduced = reduced

        #=== Create adjacency dictionary: a dictionary where each key represents a pair of vertices (labeled 0,1,2,...), and the value of each key represents the number of edges between them.
        indexedReducedList = {}
        countX,countY = 0,0
        for entry in self.reduced:
            indexedReducedList[(countX, countY)] = entry
            if countY < countX:
                countY += 1
            elif countY == countX:
                countX += 1
                countY = 0
        self.adjacencyDict = indexedReducedList

        #=== Find number of edges and vertices
        # number of edges
        self.size  = sum(self.reduced)
        # number of vertices
        self.order = int((sqrt(1+8*len(self.reduced)) - 1)/2) # this formula comes from the fact that the reduced list contains v(v+1)/2 elements where v is the number of vertices. We can find v using the quadratic formula

    def prettyprint(self):
        matrix = []
        for i in range(self.order):
            matrix += [self.reduced[int((i+1)*i/2):int((i+2)*(i+1)/2)]]
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))

    #Permute a graph's reduced list according to a given permutation of its vertices.
    def permuteVertices(self, permutation):
        permutedAdjacencyDict = {}
        for (v1,v2), numberOfEdges in self.adjacencyDict.items():
            permutedAdjacencyDict[(permutation[v1],permutation[v2])] = numberOfEdges
        for (v1,v2), numberOfEdges in permutedAdjacencyDict.items():
            if v1 < v2:
                permutedAdjacencyDict[(v2,v1)] = numberOfEdges
                del permutedAdjacencyDict[(v1,v2)]
        permutedReducedList = []
        for index in sorted(permutedAdjacencyDict):
            permutedReducedList += [permutedAdjacencyDict[index]]
        return permutedReducedList

    # Generate all permutations of vertices of this graph (i.e., all graphs in reduced list form which are isomorphic to self)
    def graphPermutations(self):
        ps = []
        for p in permutations(range(self.order)):
           ps += [self.permuteVertices(p)]
        return ps

    def isomorphic(self, other):
        pass

#Generate list of all labeled graphs with v vertices and e edges. (Note: generates ALL graphs, not those different up to isomorphism.)
#@lib.timer("allGraphs")
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
    print(graphs[0].reduced); graphs[0].prettyprint(); print("\n")
    isoClasses = [graphs[0].graphPermutations()] #isoClasses contains sets of permutations of each graph. since the set of all permutations of a graph's vertices is its isomorphism class, isoClasses contains each isomorphism class.
    for G1 in graphs: # for each G1 in graphs, if G1 not equal to any permutation of any graph in isoClasses, add its permutations to isoClasses
        for G2 in isoClasses:
            if G1.reduced in G2:
                break
        else: #this block only runs if the inner loop above exited normally; i.e., if no isomorphism was found.
            isoClasses += [G1.graphPermutations()]
            print(G1.reduced); G1.prettyprint(); print("\n")
        continue
    print(len(isoClasses), "non-isomorphic graphs found.")

## NEXT OPTIMIZATION:
#If it doesn't take too much more time, it is possible to sort out the graph you are comparing and check that the numbers of edges between vertices match up. (e.g., if a graph G1 has a pair of vertices with 5 edges between then but another graph G2 has no pairs of vertices with 5 edges between them, then G1 and G2 are definitely not isomorphic. You can check this by sorting the reduced lists and making sure they are equal. If they are, then you can continue checking to see if the graph is equal to any of the (unsorted) permutations of the other graph.)

#This optimization can go even further. When generating the binary lists which will eventually be converted into reduced lists, one knows that if the number of zeroes in the two binary lists differ, then clearly the resultant graphs cannot be isomorphic.
