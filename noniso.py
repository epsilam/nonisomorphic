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

        #=== Check that at least one of binlist or reduced has been passed.
        if binlist is None and reduced is None:
            raise "No arguments passed. User must provide either binary list representation or reduced list representation."

        #=== Store the binary list representation and determine reduced list representation.
        if reduced is None and binlist is not None:
            self.binlist = binlist
            self.reduced, k = [], 0
            sequence = self.binlist + [1] #Since it counts 0s before each 1, we need to make sure there is a 1 at the end so that the last couple of 0s are counted.
            for digit in sequence:
                if digit == 0: k += 1
                elif digit == 1: self.reduced, k = self.reduced + [k], 0

        # If user passed a value to reduced, then use this instead of calculating the reduced list. This was primarily used for debugging purposes.
        elif reduced is not None: self.reduced = reduced

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
    binSeqs   = lib.binarySequences(binlength, binsum)
    for binlist in binSeqs:
        graph = Graph(binlist)
        yield graph

#Generate list of all different undirected graphs (including multigraphs) of v vertices and e edges up to isomorphism.
#Set call with pr=True to print all the graphs, and pr=False to hide the graphs.
@lib.timer
def nonIsomorphicGraphs(v: int, e: int, pr=False):
    if v < 1: raise Exception("Vertex count too low. At least 1 vertex required.")
    if e < 0: raise Exception("Edge count too low. At least 0 edges required.")

    graphs = allGraphs(v,e)
    firstGraph = next(graphs)
    firstGraph.createGraphPermutations()
    firstGraph.sort()
    isoClasses = [firstGraph] # Since isomorphism is an equivalence relation, each isomorphism class can be represented by any of the graphs in it. Thus, if we find a new graph which is non-isomorphic to each permutation of each existing graph in isoClasses, it must be a member of a new isomorphism class.
    graphCounter = 1
    if pr == True: print(firstGraph.reduced, "Count:", graphCounter)
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
            graphCounter += 1
            if pr == True: print(G1.reduced, "Count:", graphCounter)
    print(graphCounter, "non-isomorphic graphs found.")
