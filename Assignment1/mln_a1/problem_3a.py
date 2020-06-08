import networkx as nx
import csv
import matplotlib.pyplot as plt
import operator
import random


import pickle

def loadPickleFile(filepath):
	#Loads the Pcikle FIle
	print("Loading the pickle file from",filepath,"...........")
	pickle_in = open(filepath,"rb")
	example_dict = pickle.load(pickle_in)
	print("Loaded the pickle File")
	return example_dict

def dumpPickleFile(data,filepath):
	#Dumps the Pickle FIle
	pickle_out = open(filepath,"wb")
	print("Dumping the Pickle file into ",filepath,"...........")
	pickle.dump(data, pickle_out)
	print("Dumped the pickle File")
	pickle_out.close() 

def makeERGraph(n,L):
	ERgraph = nx.Graph()
	
	print("Adding Nodes......")
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
		
		ERgraph.add_edge(int(RandomNumber1),int(RandomNumber2))
	return ERgraph



def graphInfo(graph,weighted = False):
	print("Number of Vertices = ",graph.number_of_nodes())
	print("Number of Edges = ",graph.number_of_edges())
	print("Number of Connected Components = ",nx.number_connected_components(graph))
	#print("Average Degree = ",nx.average_degree_connectivity(graph))
	if weighted  == False:
		print("Size of Unweighted Graph = ",graph.size(weight = None))
	else:
		print("Size of Weighted Graph = ",graph.size(weight = "weight"))
		averageWeightedDegree = nx.average_degree_connectivity(graph,weight = "weight")
		print("Average Weighted Degree = ",averageWeightedDegree)


ERgraph = makeERGraph(5242,14484)

#Generating standard graph info
graphInfo(ERgraph)
#dumpPickleFile(ERgraph,"problem_3a_graph.pkl")