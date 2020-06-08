import networkx as nx
import csv
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression
import numpy as np

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
	#Make a formalized edge list 
	edge_list = []
	for edge in edges:
		node1 = int(edge[0])
		node2 = int(edge[1])
		edge_tup = (node1,node2) 
		edge_list.append(edge_tup)
	return edge_list


def convert_to_undirected(DiGraph,reciprocal = False, as_view = False):
	# Needed so as convert Directed graph to undirected for certain parts
	graph = DiGraph.to_undirected(reciprocal = reciprocal, as_view = as_view)
	return graph


def get_indegrees(DiGraph):
	# Returns all the indegrees of a DiGraph in a list of tuples with a format of (v,correspoding indegree)
	indegrees = DiGraph.in_degree(nbunch=None, weight=None)
	return indegrees

def get_outdegrees(DiGraph):
	# Returns all the outdegrees of a DiGraph in a list of tuples with a format of (v,correspoding outdegree)
	outdegrees = DiGraph.out_degree(nbunch=None, weight=None)
	return outdegrees


def make_dictionary(degree_tuples):
	# Convert Tuples in to dictionary
	degree_dict = {}
	for deg_tuple in degree_tuples:
		v = deg_tuple[0]
		deg = deg_tuple[1]
		if v not in degree_dict:
			degree_dict[v] = deg
		else:
			print("ERROR",degree_dict[v],v,deg)
	return degree_dict


def count_dict(outdegrees):
	#Make a count_dictionary which is the degee_distribution
	degree_dist = {}
	for tup in outdegrees:
		v = tup[0]
		degree = tup[1]
		if degree not in degree_dist:
			degree_dist[degree] = 1
		else:
			degree_dist[degree] += 1
	return degree_dist


def make_degree_distribution(degree_dist):
	#make  sorted lists of degree distribution 
	degree_dist1 = sorted(degree_dist.keys())
	degrees = [];counts = []
	for t in degree_dist1:
		degree = t;count = degree_dist[t]
		counts.append(count);degrees.append(degree)
	return degrees,counts



#Loaded a Empty directed Graph from networkx 
DG = nx.DiGraph()
edges = readFile("wiki-Vote.txt")
edge_list = make_edge_list(edges)

# Adding edges to directed graph
DG.add_edges_from(edge_list)

outdegrees = get_outdegrees(DG)
# outdegrees1 = make_dictionary(outdegrees)
degree_dist = count_dict(outdegrees)
degrees,counts = make_degree_distribution(degree_dist)


include_zero = True

#Not includind 0 since log 0 is undefined otherwise the line fit would be different
degrees[0] = 0.5

log_degrees = np.log(degrees)
log_counts = np.log(counts)

if include_zero == False:
	log_degrees = np.log(degrees[1:])
	log_counts = np.log(counts[1:])

#Plotting the degree distribution 
plt.scatter(log_degrees,log_counts,marker='x',color = 'r')
plt.title("Degree Distribution plot on Log Log Scale")
plt.xlabel("degree - logscale")
plt.ylabel("nfnodes - logscale ")

#Converting into 2d Array in order to apply Linear Regression
log_degrees = np.array(log_degrees).reshape(-1,1)
log_counts = np.array(log_counts).reshape(-1,1)

#Applying Sklearn Linear REgression and pedicting the output values
reg = LinearRegression(normalize = False).fit(log_degrees,log_counts)
predictions  = reg.predict(log_degrees)

plt.plot(log_degrees,predictions,color='green',linewidth = 2)

#plt.savefig("Graphs/1b/Degree_Distribution_plot_2.png")
plt.show()


