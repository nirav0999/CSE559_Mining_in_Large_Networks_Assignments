import networkx as nx
import csv
import matplotlib.pyplot as plt
import operator
import random
import numpy as np

import pickle






#PS - a lot of functions are of problem 3a,b,c,d this is so in order to recreate all graphs in demo 
# For their documentation see respective files 

def loadPickleFile(filepath):
	print("Loading the pickle file from",filepath,"...........")
	pickle_in = open(filepath,"rb")
	example_dict = pickle.load(pickle_in)
	print("Loaded the pickle File")
	return example_dict

def dumpPickleFile(data,filepath):
	pickle_out = open(filepath,"wb")
	print("Dumping the Pickle file into ",filepath,"...........")
	pickle.dump(data, pickle_out)
	print("Dumped the pickle File")
	pickle_out.close() 

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
	edge_list = []
	for edge in edges:
		node1 = int(edge[0])
		node2 = int(edge[1])
		edge_tup = (node1,node2) 
		edge_list.append(edge_tup)
	return edge_list


def make3a_Graph(n,L):
	ERgraph = nx.Graph()
	print("Adding Nodes......")

	#Adding all the nodes
	for node in range(n):
		ERgraph.add_node(node)
	print("Adding Edges......")
	
	edge_list = []
	for edge in range(L):
		RandomNumber1 = 0
		RandomNumber2 = 0
		tup = (RandomNumber2,RandomNumber1)
		rev_tup = (RandomNumber1,RandomNumber2)

		#Checking for self - loops 
		#Checking for already created Edge in graph
		while(RandomNumber2 == RandomNumber1 or (tup in edge_list) or (rev_tup in edge_list)):
			
			#Generating Random Edges
			RandomNumber1 = random.randint(0,n)
			RandomNumber2 = random.randint(0,n)
			tup = (RandomNumber2,RandomNumber1)
			rev_tup = (RandomNumber1,RandomNumber2)

		edge_list.append(tup)

		if edge % 1000 == 0:
			print("Adding edge between ",RandomNumber1,"and",RandomNumber2,"--------",edge)
		
		#Adding the edge
		ERgraph.add_edge(int(RandomNumber1),int(RandomNumber2))
	return ERgraph

def make3b_Graph(n):
	# Documented with a print statements and as in problem 3b
	ERgraph = nx.Graph()
	print("Adding Nodes......")
	for node in range(n):
		ERgraph.add_node(node)

	print("Making a circle with consecutive edges.....")
	
	ERgraph.add_edge(0,n-1)
	for node in range(1,n - 1):
		ERgraph.add_edge(node-1 ,node)

	print("Number of Edges 1 = ",ERgraph.number_of_edges())
	print("Making a circle with bouncing edges.....")
	
	ERgraph.add_edge(1,n-1)
	ERgraph.add_edge(0,n-2)

	for node in range(n-3):
		ERgraph.add_edge(node,node + 2)

	print("Adding Random Edges......")
	print("Number of Edges 2 = ",ERgraph.number_of_edges())

	for edge_no in range(4000):
		RandomNumber1 = random.randint(0,n)
		RandomNumber2 = random.randint(0,n)
		while(RandomNumber2 == RandomNumber1 or ERgraph.has_edge(int(RandomNumber1),int(RandomNumber2)) == True):
			RandomNumber1 = random.randint(0,n)
			RandomNumber2 = random.randint(0,n)
		if edge_no % 1000 == 0:
			print("Adding edge between ",RandomNumber1,"and",RandomNumber2,"--------",edge_no)
		ERgraph.add_edge(int(RandomNumber1),int(RandomNumber2))

	print("Number of Edges 3 = ",ERgraph.number_of_edges())
	return ERgraph

def make3c_graph():
	#Makes Arxiv Graph 
	graph = nx.Graph()
	edges = readFile("arxiv.txt")
	edge_list = make_edge_list(edges)
	graph.add_edges_from(edge_list)
	#graphInfo(graph)
	return graph	


def make_subgraph(graph,nodes):
	#Makes a Subgraph
	subgraph = graph.subgraph(nodes)
	return subgraph

def avg_clustering_coefficient(graph):
	#Making a subgraph of neighbors of vertex v and then calculating it's nfedges and nfnodes
	# Applies the formuls 
	nodes = graph.nodes()
	avg_clus_coeff = 0

	for node in nodes:

		#Get all neighbors of graph
		neighbors = graph.neighbors(node)

		#Make a subgraph consisting of only neighbors
		subgraph_of_neighbors = make_subgraph(graph,neighbors)

		nfedges = subgraph_of_neighbors.number_of_edges()
		nfnodes = subgraph_of_neighbors.number_of_nodes()
		
		if nfnodes > 1:
			#Clsutering Coefficient is Calculated
			clustering_coeff = 2*nfedges/(nfnodes*(nfnodes - 1))
		else:
			# for 1 neighbor add nothing - redundant code  but important for understanding
			clustering_coeff = 0

		avg_clus_coeff += clustering_coeff

	return avg_clus_coeff/len(nodes)

def graphInfo(graph,weighted = False):
	print("Number of Vertices = ",graph.number_of_nodes())
	print("Number of Edges = ",graph.number_of_edges())
	print("Number of Connected Components = ",nx.number_connected_components(graph))
	if weighted  == False:
		print("Size of Unweighted Graph = ",graph.size(weight = None))
	else:
		print("Size of Weighted Graph = ",graph.size(weight = "weight"))
		averageWeightedDegree = nx.average_degree_connectivity(graph,weight = "weight")
		print("Average Weighted Degree = ",averageWeightedDegree)





p3a_graph = loadPickleFile("problem_3a_graph.pkl")#make3a_Graph(5242,14484)
avg_cc_3a = avg_clustering_coefficient(p3a_graph)
print("Average Clustering Coefficient 3a self-made= ",avg_cc_3a)
print("Average Clustering Coefficient 3a library = ",nx.average_clustering(p3a_graph))
print("---------------------------------------------------------------")
p3b_graph = loadPickleFile("problem_3b_graph.pkl")
avg_cc_3b = avg_clustering_coefficient(p3b_graph)
print("Average Clustering Coefficient 3a self-made= ",avg_cc_3b)
print("Average Clustering Coefficient 3a library = ",nx.average_clustering(p3b_graph))
print("---------------------------------------------------------------")
p3c_graph = make3c_graph()
avg_cc_3c = avg_clustering_coefficient(p3c_graph)
print("Average Clustering Coefficient 3a self-made= ",avg_cc_3c)
print("Average Clustering Coefficient 3a library = ",nx.average_clustering(p3c_graph))
#print("Average Clustering Coefficient 3c = ",avg_cc_3c,nx.average_clustering(p3c_graph,count_zeros=True),nx.average_clustering(p3c_graph,count_zeros=False))









