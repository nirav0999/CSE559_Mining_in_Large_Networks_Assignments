import networkx as nx
import csv
import numpy as np 
import pickle
import networkx as nx
import csv
import matplotlib.pyplot as plt
import operator
import random
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
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


def appendToCSV(filepath,row):
	with open(filepath,"a",buffering = 1) as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)

def openCSVfile(filepath):
	with open(filepath,"r") as csvfile:
		rows =  csv.reader(csvfile,delimiter = "\t")
		return list(rows)


def graphInfo(graph,weighted = False):
	print("Number of Vertices = ",graph.number_of_nodes())
	print("Number of Edges = ",graph.number_of_edges())
	#print("Number of Connected Components = ",nx.number_connected_components(graph))
	#print("Average Degree = ",nx.average_degree_connectivity(graph))


def calcEdgeAddProb(MGraph):

	#Dictionary of new Degree 
	degrees  = dict(MGraph.degree())

	#Probabilities of addition of new edge
	new_edge_probabilities = []

	#total degree
	total_degree = 0
	
	#Calculating 
	for v in degrees:
		degree = degrees[v]
		total_degree += degree
		new_edge_probabilities.append(0)

	#Calculating Probabbilites of addition of new node
	for v in degrees:
		new_edge_probabilities[v] = degrees[v]/total_degree
	
	return new_edge_probabilities


def nodeAcctoProb(n,prob_list):
	#return a random node according to probability
	return np.random.choice(np.arange(n), p = prob_list)


def add_new_edges(node_list,Mgraph,n):
	#Adds the new node to the graph
	Mgraph.add_node(n)
	
	#New edges to be added
	added_edge_list = []

	#Fill the new nodes list
	for node in node_list:
		
		#Tuple to be added
		t = (node,n)
		
		#Adding in edge list
		added_edge_list.append(t)
	
	#Add Edges
	MGraph.add_edges_from(added_edge_list)

	return MGraph


def make_dist(arr):
	dist = {}
	for tup in arr:
		degree = tup[1]
		if degree not in dist:
			dist[degree] = 1
		else:
			dist[degree] += 1
	return dist

def getCumulativeSet(degree_dist):
	#Make a cumulative distribution d=from an array

	degrees = []
	d = 0
	for degree in degree_dist:
		d += degree
		degrees.append(d)
	return degrees


def make_degree_dist_graph(graph,color = 'r',label = 'label',cumulative = False):
	degrees = graph.degree(weight = None)
	#Making Initial Degree Dist
	degree_dist = make_dist(degrees)

	degrees = []
	counts = []
	
	#Soring Degree Distribution
	degree_dist1 = sorted(degree_dist.keys())
	
	for t in degree_dist1:
		degree = t
		count = degree_dist[t]
		counts.append(count)
		degrees.append(degree)


	if cumulative == True:
		#Check Cumulative
		counts = getCumulativeSet(counts)
		plt.scatter(degrees,counts,c = color,marker = 'X',label=label)
		plt.title("Cumulative Degree Distribution plot")
		plt.xlabel("Cumulative Degree")
		plt.ylabel("#nodes")

	else:

		log_degrees = np.log(degrees)
		log_counts = np.log(counts)

		#return log_degrees,log_counts
		plt.scatter(log_degrees,log_counts,c = color,marker = 'X',label=label)
		plt.title("Degree Distribution plot")
		plt.xlabel("Degree")
		plt.ylabel("#nodes")

		#Converting into 2d Array in order to apply Linear Regression
		log_degrees = np.array(log_degrees).reshape(-1,1)
		log_counts = np.array(log_counts).reshape(-1,1)

		#Applying Sklearn Linear REgression and pedicting the output values
		reg = LinearRegression(normalize = False).fit(log_degrees,log_counts)
		predictions  = reg.predict(log_degrees)

		plt.plot(log_degrees,predictions,color = 'black',linewidth = 2)


def getAvgClusteringCoefficient(graph):
	return nx.average_clustering(graph)


def makeBAModel(MGraph,n_max = 10000,m = 4,multi = True):
	
	#Average Clustering Coefficient at each time Stamp
	avg_cc_per_timestamp = []

	#Degree Dist 
	examine0 = []
	examine104 = []
	examine1004 = []
	examine5004 = []

	#print('here')

	while (len(MGraph.nodes()) < n_max):

		#print('here1')
		n = len(MGraph.nodes())


		#returns probability of attachment of new edges
		prob_list = calcEdgeAddProb(MGraph)

		#New edges to be added
		edges_to_add_to_node = []

		#Getting m more nodes to be added
		for i in range(m):

			#Gettting a new node	
			node = nodeAcctoProb(n,prob_list)
			if multi == True:

				#If node is already in list no problem coz multi edges are allowed
				edges_to_add_to_node.append(node)
			
			else:
				# Node is already in list then it is a problem 
				while(node in edges_to_add_to_node):
					node = nodeAcctoProb(n,prob_list)

				#Adding nodes to which edges have to 
				edges_to_add_to_node.append(node)

		#Add new Edges into the graph
		Mgraph = add_new_edges(edges_to_add_to_node,MGraph,n)
		
		if (n + 1)% 10 == 0:
			avg_clustering = nx.average_clustering(Mgraph)
			avg_cc_per_timestamp.append(avg_clustering) 
			print("Edges to add to nodes = ",edges_to_add_to_node)
			print("Number of nodes = ",len(MGraph.nodes()))
			print("Average Clustering = ",avg_clustering)

		if (n == 99) or (n == 999) or (n == 9999):
			#dumpPickleFile(MGraph,"graph_at_" + str(n) + "_nodes.pkl")
			print('Number of Nodes =',n + 1)
			#make_degree_dist_graph(Mgraph,color = 'r',label = str(n + 1))

		if n >= 4:
			degree0 = MGraph.degree(0)
			examine0.append(degree0)

		if n + 1 >= 104:
			degree104 = MGraph.degree(103)
			examine104.append(degree104)

		if n + 1 >= 1004:
			degree1004 = MGraph.degree(1003)
			examine1004.append(degree1004)

		if n + 1 >= 5004:
			degree5004 = MGraph.degree(5003)
			examine5004.append(degree5004)

	# dumpPickleFile(examine0,"degree0.pkl")
	# dumpPickleFile(examine104,"degree104.pkl")
	# dumpPickleFile(examine1004,"degree1004.pkl")
	# dumpPickleFile(examine5004,"degree5004.pkl")
	# dumpPickleFile(avg_cc_per_timestamp,"average_clustering_coefficient.pkl")
	return MGraph



def loadGraph():
	MGraph = nx.Graph()	
	edge_list = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
	MGraph.add_edges_from(edge_list)
	graphInfo(MGraph)
	return MGraph 


def make_DDgraphs():
	G1 = loadPickleFile("graph_at_99_nodes.pkl")
	G2 = loadPickleFile("graph_at_999_nodes.pkl")
	G3 = loadPickleFile("graph_at_9999_nodes.pkl")
	make_degree_dist_graph(G1,color = 'r',label = "graph @ t = 100",cumulative = False)
	make_degree_dist_graph(G2,color = 'b',label = "graph @ t = 1000",cumulative = False)
	make_degree_dist_graph(G3,color = 'g',label = "graph @ t = 10000",cumulative = False)
	plt.legend()
	plt.show()


def makeAvgClusteringCoefficentGraph(log = False):
	avgcc = loadPickleFile("average_clustering_coefficient.pkl")
	arr = []
	cc = []

	for i in range(9,9999,10):
		arr.append(i)
		cc.append(avgcc[i])

	if log == False:
		plt.xlabel("Timestamp")
		plt.ylabel("Average Clustering Coefficient")
		plt.title("Average Clustering Coefficient per timestamp")
		#plt.scatter(np.log(arr),np.log(cc),marker = 'X',label = "Initial Node",color = "r")
		plt.scatter(arr,cc,marker = 'X',label="Avg cc per t for BA graph",color = "r")
		plt.legend()
		plt.show()

	else:

		log_degrees = np.log(arr)
		log_counts = np.log(cc)

		#return log_degrees,log_counts
		plt.scatter(log_degrees,log_counts,c = "r",marker = 'X',label = "Avg cc per t log-log scale")
		plt.title("Average CLustering Coefficient per timestamp - log log Scale")
		plt.xlabel("Timestamp - log")
		plt.ylabel("#nodes - log")

		#Converting into 2d Array in order to apply Linear Regression
		log_degrees = np.array(log_degrees).reshape(-1,1)
		log_counts = np.array(log_counts).reshape(-1,1)

		#Applying Sklearn Linear REgression and pedicting the output values
		reg = LinearRegression(normalize = False).fit(log_degrees,log_counts)
		predictions  = reg.predict(log_degrees)

		plt.plot(log_degrees,predictions,color = 'black',linewidth = 2)
		plt.legend()
		plt.show()



def makeCumulativeDegreeDistribution():
	#Loading all the graphs
	G1 = loadPickleFile("graph_at_99_nodes.pkl")
	G2 = loadPickleFile("graph_at_999_nodes.pkl")
	G3 = loadPickleFile("graph_at_9999_nodes.pkl")


	#Making Cumulative Degree Distributions
	make_degree_dist_graph(G1,color = 'r',label = 'Cumulative Degree Distribution @ t = 100',cumulative = True)
	make_degree_dist_graph(G2,color = 'b',label = 'Cumulative Degree Distribution @ t = 1000',cumulative = True)
	make_degree_dist_graph(G3,color = 'g',label = 'Cumulative Degree Distribution @ t = 10000',cumulative = True)

	plt.legend()
	plt.show()


def makeDegreeTimeGraphs():
	#Loading all Degree Graphs
	degree0 = loadPickleFile("degree0.pkl")
	degree104 = loadPickleFile("degree104.pkl")
	degree1004 = loadPickleFile("degree1004.pkl")
	degree5004 = loadPickleFile("degree5004.pkl")

	plt.xlabel("Timestamp")
	plt.ylabel("Degree")
	plt.title("Degrees of various nodes at different timestamps")

	plt.scatter(np.arange(0,len(degree0)),np.array(degree0),marker = 'X',label="Initial Node",color = "r")
	plt.scatter(np.arange(100,len(degree104)+100),np.array(degree104),marker = 'X',label = " Node @ t = 100",color = "b")
	plt.scatter(np.arange(1000,len(degree1004)+1000),np.array(degree1004),marker = 'X',label = "Node @ t = 1000",color = "g")
	plt.scatter(np.arange(5000,len(degree5004)+5000),np.array(degree5004),marker = 'X',label =  "Node @ t = 5000",color = "black")

	plt.legend()
	plt.show()
	
	#loadPickleFile("degree5004.pkl")


plt.rcParams['font.family'] = "Times New Roman"
plt.rcParams['font.size'] = 25
# MGraph = loadGraph()
# calcEdgeAddProb(MGraph)
# Mgraph = makeBAModel(MGraph,multi = False)
# graphInfo(Mgraph)
# plt.show()

#Degree Distributions
make_DDgraphs()
#Make Cumulative Degree Distributions
makeCumulativeDegreeDistribution()
makeAvgClusteringCoefficentGraph(log = False)
makeAvgClusteringCoefficentGraph(log = True)
makeDegreeTimeGraphs()
