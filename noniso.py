import srclib as lib
from numpy import sqrt
from itertools import permutations
from collections import Counter

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
            self.reduced, k = [], 0
            sequence = self.binlist + [1] #Since it counts 0s before each 1, we need to make sure there is a 1 at the end so that the last couple of 0s are counted.
            for digit in sequence:
                if digit == 0: k += 1
                elif digit == 1: self.reduced, k = self.reduced + [k], 0

        # If user passed a value to reduced, then use this instead of calculating the reduced list. This was primarily used for debugging purposes.
        elif reduced != None: self.reduced = reduced

        #=== Create adjacency dictionary: a dictionary where each key represents a pair of vertices (labeled 0,1,2,...), and the value of each key represents the number of edges between them.
        self.adjacencyDict, v1, v2 = {}, 0, 0
        for edges in self.reduced:
            self.adjacencyDict[(v1, v2)] = edges
            if v2 < v1: v2 += 1
            elif v2 == v1: v1 += 1; v2 = 0

        #=== Initialize variable graphPermutations: not computed now to save resources. IMPORTANT: Before using, make sure to call self.createGraphPermutations()
        self.graphPermutations = []

        #=== Initialize variable reducedSorted: computed in self.sort() To efficiently verify that two graphs are non-isomorphic, we can check if their sorted reduced list representations differ. If they do, they they are definitely non-isomorphic.
        self.reducedSorted = None

    def prettyprint(self):
        matrix = []
        for i in range(self.order): matrix += [self.reduced[int((i+1)*i/2):int((i+2)*(i+1)/2)]]
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
    def createGraphPermutations(self):
        numberOfVertices = int((sqrt(1+8*len(self.reduced)) - 1)/2) # calculated via quadratic formula; given v vertices, reduced list contains v(v+1)/2 elements
        for p in permutations(range(numberOfVertices)):
            self.graphPermutations += [self.permuteVertices(p)]

    def sort(self):
        self.reducedSorted = Counter(self.reduced)

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
#Set call with pr=True to print all the graphs, and pr=False to hide the graphs.
@lib.timer
def nonIsomorphicGraphs(v, e, pr=False):
    graphs = allGraphs(v,e)
    graphs[0].createGraphPermutations()
    graphs[0].sort()
    isoClasses = [graphs[0]] # Since isomorphism is an equivalence relation, each isomorphism class can be represented by any of the graphs in it. Thus, if we find a new graph which is non-isomorphic to each permutation of each existing graph in isoClasses, it must be a member of a new isomorphism class.
    if pr == True:
        print(graphs[0].reduced); graphs[0].prettyprint(); print("\n")
    for G1 in graphs: # for each G1 in graphs, if G1 not equal to any permutation of any graph in isoClasses, add its permutations to isoClasses
        G1.sort()
        for G2 in isoClasses:
            if G1.reducedSorted != G2.reducedSorted:
                continue
            if G1.reduced in G2.graphPermutations:
                break
        else: #this block only runs if the inner loop above exited normally; i.e., if no isomorphism was found.
            G1.createGraphPermutations()
            isoClasses += [G1]
            if pr == True:
                print(G1.reduced); G1.prettyprint(); print("\n")
    print(len(isoClasses), "non-isomorphic graphs found.")

## NEXT OPTIMIZATION:
#If it doesn't take too much more time, it is possible to sort out the graph you are comparing and check that the numbers of edges between vertices match up. (e.g., if a graph G1 has a pair of vertices with 5 edges between then but another graph G2 has no pairs of vertices with 5 edges between them, then G1 and G2 are definitely not isomorphic. You can check this by sorting the reduced lists and making sure they are equal. If they are, then you can continue checking to see if the graph is equal to any of the (unsorted) permutations of the other graph.)

#This optimization can go even further. When generating the binary lists which will eventually be converted into reduced lists, one knows that if the number of zeroes in the two binary lists differ, then clearly the resultant graphs cannot be isomorphic.
