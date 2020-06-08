import networkx as nx
import basic_functions
import graph_functions
import copy
import random
import numpy as np
import itertools 
from sklearn.metrics import roc_auc_score
import copy
import matplotlib.pyplot as plt

def normalize(numpy_array):
	
	#Max Nomralization of the array
	max_value = np.amax(numpy_array)
	normalized_array = numpy_array/max_value
	return normalized_array

def calc_indexes(G,test_edges,aa = False):
	"""
	Input - 
	G  - is the graph based upon which we calculate the indexes
	test_edges -  are the edges for which we calculate the index 
	aa - whether to calculate the adamic adder index or not 

	Calculates all the indixes of the graph for the test_edgessuch as 
	1) Common Neighbors
	2) Jaccard
	3) Preferential Attachment
	4) Adamic Adder
	"""

	#All indexes stored as a dictionary
	indexes = {}

	#Initiazing 
	jaccard_arr = []
	common_arr = []
	preferential_arr = []
	adamic_adder = []

	aa1 = nx.adamic_adar_index(G,test_edges)
	jc = nx.jaccard_coefficient(G,test_edges)
	pa = nx.preferential_attachment(G,test_edges)


	for edge in test_edges:
		
		#Loading the nodes
		node1 = edge[0];node2 = edge[1];node_list = [node1,node2]
		#Neighbors of the nodes
		node1_neighbors = set(list(G.neighbors(node1)));node2_neighbors = set(list(G.neighbors(node2)))
		#Union of the neighbors
		union_neighbors = list(node1_neighbors.union(node2_neighbors))
		#Intersection of the neighbors
		intersection_neighbors = list(node1_neighbors.intersection(node2_neighbors))
		
		#Jaccard Index
		jaccard_index = 0

		if len(union_neighbors) != 0:
			jaccard_index =  len(intersection_neighbors)/len(union_neighbors)
		
		#Common Neighbors
		common_neighbors = len(intersection_neighbors)
		#Preferential Attachment
		preferential_attachment = len(node1_neighbors) * len(node2_neighbors)
		
		#Appending the indexes into the arrays
		jaccard_arr.append(jaccard_index)
		common_arr.append(common_neighbors)
		preferential_arr.append(preferential_attachment)

		#if adamic_adder is to be calculated
		if aa == True:
			adamic_add = 0
			for neighbor in intersection_neighbors:
				nfneighbors_of_neighbors = len(list(G.neighbors(neighbor)))
				#Adamic adder doesn't make sense for nfneighbors_of_neighbors == 0 or 1
				if nfneighbors_of_neighbors != 1 and nfneighbors_of_neighbors != 0:
					aa_score = 1/np.log(nfneighbors_of_neighbors)
					adamic_add += aa_score
			adamic_adder.append(adamic_add)

	indexes['jaccard_index'] = jaccard_arr
	indexes['common_neighbors'] = common_arr
	indexes['preferential_attachment'] = preferential_arr
	indexes['adamic_adder'] = adamic_adder

	# print(adamic_adder[:10],aa[:10])
	# print(jaccard_arr[:10],jc[:10])
	# print(preferential_arr[:10],pa[:10])
	#print(indexes['adamic_adder'])
	#print(adamic_adder)
	#print(jaccard_arr)

	# for u, v, p in jc:
	# 	print(u, v, p)
	# 	ind = test_edges.index((u,v))
	# 	print(jaccard_arr[ind],ind)
	
	# for u, v, p in pa:
	# 	print(u, v, p)
	# 	ind = test_edges.index((u,v))
	# 	print(preferential_arr[ind],ind)

	# for u, v, p in aa1:
	# 	print(u, v, p)
	# 	ind = test_edges.index((u,v))
	# 	print(adamic_adder[ind],ind)


	return indexes


def get_all_nonexistent_edge_list(G):
	"""
	All edges which are NOT in G
	"""
	
	#Edge list of Graph
	edge_list = list(G.edges())
	
	#Node list of Graph
	graph_nodelist = list(G.nodes())
	
	#All Possible Edge Combinations
	edge_combinations = itertools.combinations(graph_nodelist,2)
	edge_combinations1 = copy.deepcopy(edge_combinations)
	
	#Non existent edge list = all possible edge combinations -  current edge list 
	nonexistent_edge_list = set(edge_combinations) - set(edge_list)
	#print("#edge combinations = ",len(list(edge_combinations1)))
	
	return list(nonexistent_edge_list)

def randomly_remove_edges(edges,percentage):
	"""
	Randomly remove  a percentage removes of edges
	"""
	edges = list(edges)
	nfedges = len(edges)
	nfnodes_to_remove = int(percentage * nfedges * (1/100))
	nfnodes_removed = 0
	removed_edges = []
	
	while(nfnodes_removed < nfnodes_to_remove):
		random_item_from_list = random.choice(edges)
		removed_edges.append(random_item_from_list)
		edges.remove(random_item_from_list)
		nfnodes_removed += 1

	return edges,removed_edges

def calculate_probability(list1):
	"""
	Apply Softmax to calculate the probability
	"""
	probs = np.exp(list1)/sum(np.exp(list1))
	return probs

def make_ground_truth(nfpositive_samples,nf_negative_samples):
	"""
	Make Ground Truth of [1 1 1 1 ..... 0 0 0 0 0]
	where 1 is the positive sample
	where 0 is the negative sample
	"""
	ground_truth = []
	for i in range(nfpositive_samples):
		ground_truth.append(1)
	for i in range(nf_negative_samples):
		ground_truth.append(0)
	return np.array(ground_truth)


def make_initial_graphs(rows):
	int_edge_list = []
	node_list = set()
	for row in rows:
		node1 = int(row[0])
		node2 = int(row[1])
		edge = (node1,node2)
		node_list.add(node1)
		node_list.add(node2)
		int_edge_list.append(edge)
	
	int_edge_list.sort()
	
	node_list = list(node_list)
	node_list.sort()

	G = nx.Graph(int_edge_list)
	G1 =  nx.Graph()
	G1.add_nodes_from(node_list)

	#print("#nodes of G = ",len(G.nodes()))
	#print("#nodes of G1 = ",len(G1.nodes()))

	return G,G1,node_list


#------------------------------PARAMETERS------------------------------

percentages = [25,35,45,55]


#Path of edge list
edge_list_path = "../data/fb-pages-food/fb-pages-food.edges"


#k-fold
k = 10

x = []
y = []


for percentage in percentages:

	#-----------------------------LOAD GRAPH------------------------------

	jaccard_index_roc_all = []
	common_neighbors_index_roc_all = []
	preferential_attachment_roc_all = []
	adamic_adder_roc_all = []

	print("--------------------","Percentage = ",percentage,"----------------------")
	
	for i in range(k):

		#Rows from the edge list
		rows = basic_functions.openCSVfile(edge_list_path)

		#Make the graphs
		G,G1,node_list = make_initial_graphs(rows)

		#print("Number of edges in G = ",len(G.edges()))


		#print("--------------------------------------------------",i,"--------------------------------------------")

		#New_edge_list with edges removed and the removed edges are considered as positive samples
		train_edges, positive_edges = randomly_remove_edges(G.edges(),percentage)
		
		#Adding edges to G1 
		G1.add_edges_from(train_edges)

		#print("Number of edges in G1= ",len(G1.edges()))
		
		#Edge Lists
		G_edge_list = nx.to_numpy_matrix(G, nodelist = node_list)
		G1_edge_list = nx.to_numpy_matrix(G1, nodelist = node_list)
		
		#Negative Edge Set
		negative_edges = get_all_nonexistent_edge_list(G)
		
		#Number of Positive Edges
		nfpositive_edges = len(positive_edges)
		#Number of Negative Edges
		nfnegative_edges = len(negative_edges)

		print("Number of Positive edges = ",nfpositive_edges)
		print("Number of Negative edges = ",nfnegative_edges)
		
		#Make Test Set edges
		test_edges = positive_edges + negative_edges
		print("Number of test edges = ",len(test_edges))
		print("Number of train_edges = ",len(train_edges))

		#No Common edges between positive samples and negative samples
		assert(len(set(positive_edges).intersection(negative_edges)) == 0)
		
		# No Common edges between train_edges and test_edges
		assert(len(set(train_edges).intersection(test_edges)) == 0)

		# Making Ground Truth
		ground_truth = make_ground_truth(nfpositive_edges,nfnegative_edges)

		#print("Size of Ground Truth = ",len(ground_truth))

		#Indexes are 
		indexes = calc_indexes(G1,test_edges,True)

		#Index
		jaccard_index = indexes['jaccard_index']
		common_arr	= indexes['common_neighbors'] 
		preferential_arr = indexes['preferential_attachment'] 
		adamic_adder = indexes['adamic_adder']

		#Normalizing rhe indexes
		jaccard_index = normalize(jaccard_index)
		common_arr = normalize(common_arr)
		preferential_arr = normalize(preferential_arr)
		adamic_adder = normalize(adamic_adder)

		#Calculating the indexes
		jaccard_index_roc = roc_auc_score(ground_truth, jaccard_index)
		common_neighbors_index_roc = roc_auc_score(ground_truth, common_arr)
		preferential_attachment_roc = roc_auc_score(ground_truth, preferential_arr)
		adamic_adder_roc = roc_auc_score(ground_truth, adamic_adder)

		#
		jaccard_index_roc_all.append(jaccard_index_roc)
		common_neighbors_index_roc_all.append(common_neighbors_index_roc)
		preferential_attachment_roc_all.append(preferential_attachment_roc)
		adamic_adder_roc_all.append(adamic_adder_roc)

		#print(jaccard_index_roc_all,common_neighbors_index_roc_all,preferential_attachment_roc_all,adamic_adder_roc_all)
	
	avg_ja_roc = np.mean(jaccard_index_roc_all)
	avg_cn_roc = np.mean(common_neighbors_index_roc_all)
	avg_pa_roc = np.mean(preferential_attachment_roc_all)
	avg_aa_roc = np.mean(adamic_adder_roc_all)

	print("Percentage = ",percentage)
	print("Average over",k,"folds")
	print("Jaccard Index = ",avg_ja_roc)
	print("Common Neighbors = ",avg_cn_roc)
	print("Preferentail Attachment = ",avg_pa_roc)
	print("Adamic Adder = ",avg_aa_roc)
	#print(percentage,k,avg_ja_roc,avg_cn_roc,avg_pa_roc,avg_aa_roc)
	
	x.append(percentage)
	x.append(percentage)
	x.append(percentage)
	x.append(percentage)

	y.append(avg_ja_roc)
	y.append(avg_cn_roc)
	y.append(avg_pa_roc)
	y.append(avg_aa_roc)


#Make Graph
fig, ax = plt.subplots()
colors = ['blue','red','green','yellow']
labels = ['jaccard index','common neighbors','preferential attachment','Adamic Adder']

for i in range(len(x)):
	c = i%4
	if i < 4:
		ax.scatter(x[i], y[i], color = colors[c],label = labels[c])
	else:
		ax.scatter(x[i], y[i], color = colors[c])

plt.xlabel("% of Nodes Removed")
plt.ylabel("Accuracy ")
plt.legend()
plt.show()