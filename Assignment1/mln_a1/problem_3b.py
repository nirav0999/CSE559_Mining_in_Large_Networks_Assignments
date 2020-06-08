import networkx as nx
import csv
import matplotlib.pyplot as plt
import operator
import random
import pickle

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



def makeSpecialERGraph(n):
	ERgraph = nx.Graph()
	print("Adding Nodes......")
	for node in range(n):
		ERgraph.add_node(node)

	print("Making a circle with consecutive edges.....")
	
	# Adding x-1 and x edges
	ERgraph.add_edge(0,n-1)
	for node in range(1,n-1):
		ERgraph.add_edge(node-1 ,node)

	print("Number of Edges 1 = ",ERgraph.number_of_edges())
	print("Making a circle with bouncing edges.....")
	
	ERgraph.add_edge(1,n-1)
	ERgraph.add_edge(0,n-2)

	# Adding x and x+2 edges
	for node in range(n-3):
		ERgraph.add_edge(node,node + 2)

	print("Adding Random Edges......")
	print("Number of Edges 2 = ",ERgraph.number_of_edges())

	#Adding Rnadom 4k edges
	for edge_no in range(4000):
		RandomNumber1 = random.randint(0,n)
		RandomNumber2 = random.randint(0,n)

		#Check if it not a self loop
		#Check if edge already exists
		while(RandomNumber2 == RandomNumber1 or ERgraph.has_edge(int(RandomNumber1),int(RandomNumber2)) == True):
			RandomNumber1 = random.randint(0,n)
			RandomNumber2 = random.randint(0,n)


		if edge_no % 1000 == 0:
			print("Adding edge between ",RandomNumber1,"and",RandomNumber2,"--------",edge_no)
		
		ERgraph.add_edge(int(RandomNumber1),int(RandomNumber2))

	print("Number of Edges 3 = ",ERgraph.number_of_edges())
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




ERgraph = makeSpecialERGraph(5242)
graphInfo(ERgraph)
#dumpPickleFile(ERgraph,"problem_3b_graph.pkl")
