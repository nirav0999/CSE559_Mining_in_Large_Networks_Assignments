import networkx as nx
import csv

def readFile(filename):
	#Function to load the wikivote graph
	with open(filename) as file:
		lines = file.readlines()
		
		# Frst four lines are reudndant as they include no edges so removing those
		lines = lines[4:]

		# All the rest of the ines could be viewed as a csv file delimited by \t
		edges = csv.reader(lines,delimiter = "\t")
		return edges


def make_edge_list(edges):
	"""
	Makes the edge List in a structured format
	"""
	edge_list = []
	for edge in edges:
		node1 = int(edge[0])
		node2 = int(edge[1])
		edge_tup = (node1,node2)
		rev_tup = (node1,node2)
		edge_list.append(edge_tup)

	return edge_list


def convert_to_undirected(DiGraph,reciprocal = False, as_view = False):
	# Needed so as convert Directed graph to undirected for certain parts
	graph = DiGraph.to_undirected(reciprocal = reciprocal, as_view = as_view)
	return graph


def zero_degree(degree_dictionary):
	# Condition defined for the function is that node should have zero degree
	# Function can be used for both indegree or out degree
	nfnodes_with_condition = 0  
	for v in degree_dictionary:
		if v[1] == 0:#Condition 
			nfnodes_with_condition += 1
	return nfnodes_with_condition

def gt_degree(degree_dictionary):
	# Condition defined for the function is that node should have greater than 10 degree
	# Function can be used for both indegree or out degree
	nfnodes_with_condition = 0  
	for v in degree_dictionary:
		if v[1] > 10:
			nfnodes_with_condition += 1
	return nfnodes_with_condition


def get_indegrees(DiGraph):
	# Returns all the indegrees of a DiGraph in a list of tuples with a format of (v,correspoding indegree)
	indegrees = DiGraph.in_degree(nbunch=None, weight=None)
	return indegrees

def get_outdegrees(DiGraph):
	# Returns all the outdegrees of a DiGraph in a list of tuples with a format of (v,correspoding outdegree)
	outdegrees = DiGraph.out_degree(nbunch=None, weight=None)
	return outdegrees


# def nf_weakly_connected_components(DiGraph):
# 	weakly_connected_components = nx.weakly_connected_components(DiGraph)
# 	print(weakly_connected_components)
# 	return len(weakly_connected_components)

def graphInfo(graph,weighted = False):
	# Contains all the parts of the questions
	nfnodes = graph.number_of_nodes()
	nfedges = graph.number_of_edges()
	nfselfLoops = graph.number_of_selfloops()
	print("Number of Vertices = ",nfnodes)
	print("Number of Edges = ",nfedges)
	print("Number of Self Loop Edges = ",nfselfLoops)
	print("Number of NON - self Loop Edges = ",nfedges - nfselfLoops)
	
	# Number of Unique Combinations of edges such that (a,b) is considered the same as (b,a) would be equal to the number of edges in the corresponding 
	g1 = convert_to_undirected(graph)
	nfUniqueCombinatons = g1.number_of_edges()
	print("Number of Unique Combinations of edges such that (a,b) is considered the same as (b,a) = ",nfUniqueCombinatons)
	

	print("Number of Unique Combinations of edges such that a,b is NOT considered the same as b,a = ",nfedges)
	g2 = convert_to_undirected(graph,True)
	nfComEdges = g2.number_of_edges()
	print("Number of Edges such that if a,b edge exists then so does b,a edge = ",nfComEdges) 

	indegrees = get_indegrees(graph)
	outdegrees = get_outdegrees(graph)

	#print(indegrees)

	nfnodesInDegreeZero = zero_degree(indegrees)
	nfnodesOutDegreeZero  = zero_degree(outdegrees)

	nfnodesInDegreeGt10 = gt_degree(indegrees)
	nfnodesOutDegreeGt10  = gt_degree(outdegrees)

	print("Number of nodes with indegree = 0",nfnodesInDegreeZero)
	print("Number of nodes with outdegree = 0",nfnodesOutDegreeZero)

	print("Number of nodes with indegree greater than 10 = ",nfnodesInDegreeGt10)
	print("Number of nodes with outdegree greater than  10 = ",nfnodesOutDegreeGt10)

	print("Number of weakly connected components = ",nx.number_weakly_connected_components(graph))
	print("Number of strongly connected components = ",nx.number_strongly_connected_components(graph))

#Loaded a Empty directed Graph from networkx 
DG = nx.DiGraph()
edges = readFile("wiki-Vote.txt")
edge_list = make_edge_list(edges)

# Adding edges to directed graph
DG.add_edges_from(edge_list)
graphInfo(DG)