import networkx as nx
import community
import networkx.algorithms
from networkx.algorithms.community import greedy_modularity_communities
import basic_functions
import math


def sortEdgesByWeight(graph,reverse = True):
	"""
	Sort Edges by Weight
	"""
	print("Sorting Edges by Edge Weights .....")
	return sorted(graph.edges(data = True),key = lambda x: x[2]['weight'],reverse = reverse)

def sortNodesByDegree(graph,weight = "weight",reverse = True):
	"""
	Sort Nodes by Degree or Strength
	"""
	if weight == "weight":
		print("Sorting Nodes by Strength .....")
	else:
		print("Sorting Nodes by Degree.....")
	return sorted(graph.degree(weight = weight),key = lambda x: x[1], reverse = reverse)

def getAvgCoreness(list_of_vertices,corenessDict):
	"""
	Get Average Coreness of the list of vertices
	"""
	Add_coreness = 0
	for v in list_of_vertices:
		Add_coreness += corenessDict[v]
	return Add_coreness/len(list_of_vertices)


def makeSubgraph(G,nodes):
	"""
	Make Subgraph as Nodes
	"""
	return G.subgraph(nodes)

def graphInfo(graph,weighted = 2,path_lengths = False):
	"""
	Give a Basic Analysis of the Graph
	weighted = {0:"only unweighted",1:"only weighted",else:"both weighted and unweighted"}
	path_lengths = {True:""}
	"""
	graph_info = {}

	nfnodes = graph.number_of_nodes()
	nfedges = graph.number_of_edges()
	nfComponents = nx.number_connected_components(graph)
	density = nx.density(graph)

	graph_info = {
		"nfnodes" : nfnodes,
		"nfedges" : nfedges,
		"nfComponents" : nfComponents,
		"density" : density
	}

	if weighted == 0:
		unweighted_size = graph.size(weight = None)
		graph_info['unweighted_size'] = unweighted_size
	elif weighted == 1:
		weighted_size = graph.size(weight = "weight")
		graph_info['weighted_size'] = weighted_size
	else:
		unweighted_size = graph.size(weight = None)
		weighted_size = graph.size(weight = "weight")
		graph_info['unweighted_size'] = unweighted_size
		graph_info['weighted_size'] = weighted_size

	max_unweighted_node_degree = 0
	max_weighted_node_degree = 0

	if weighted == 0:
		sorted_nodes_by_unweighted_degree = sortNodesByDegree(graph,weight = None,reverse = True)

		if nfnodes >= 2:
			max_unweighted_node_degree  = sorted_nodes_by_unweighted_degree[0]
			graph_info['max_unweighted_node_degree'] = max_unweighted_node_degree
	
	elif weighted == 1:
		sorted_edges = sortEdgesByWeight(graph)
		sorted_nodes_by_weighted_degree = sortNodesByDegree(graph,weight = "weight",reverse = True)
		max_edge_weight = None
		
		if nfedges > 1:
			max_edge_weight = sorted_edges[0]
			graph_info['max_edge_weight'] = max_edge_weight

		if nfnodes >= 2:
			max_weighted_node_degree  = sorted_nodes_by_weighted_degree[0]
			graph_info['max_weighted_node_degree'] = max_weighted_node_degree
	
	else:
		sorted_edges = sortEdgesByWeight(graph)
		sorted_nodes_by_weighted_degree = sortNodesByDegree(graph,weight = "weight",reverse = True)
		sorted_nodes_by_unweighted_degree = sortNodesByDegree(graph,weight = None,reverse = True)
		max_edge_weight = None
		
		if nfedges > 1:
			max_edge_weight = sorted_edges[0] 
			graph_info['max_edge_weight'] = max_edge_weight

		if nfnodes >= 2:
			max_unweighted_node_degree  = sorted_nodes_by_unweighted_degree[0]
			max_weighted_node_degree  = sorted_nodes_by_weighted_degree[0]
			graph_info['max_unweighted_node_degree'] = max_unweighted_node_degree
			graph_info['max_weighted_node_degree'] = max_weighted_node_degree

	weighted_avg_path_length = math.inf
	unweighted_avg_path_length = math.inf 

	if nfComponents == 1 and path_lengths == False:
		weighted_avg_path_length = nx.average_shortest_path_length(graph,weight = "weight")
		unweighted_avg_path_length = nx.average_shortest_path_length(graph,weight = None)
		graph_info['weighted_avg_path_length'] = weighted_avg_path_length
		graph_info['unweighted_avg_path_length'] = unweighted_avg_path_length

	return graph_info


def makeComponents(G):
	"""
	Make Component Subgraphs of G
	"""
	subgraphs = []
	for c in nx.connected_components(G):
		subgraphs.append(G.subgraph(c))
	return subgraphs

def allComponentsInfo(graph):
	"""
	Give all the info of the components
	"""
	components = makeComponents(graph)
	allCompInfo = {}
	for component_no,component in enumerate(components):
		compInfo = graph_info(component)
		allCompInfo["comp_" + str(component_no)] = compInfo
	return allCompInfo


#--------------------------------Community Functions-----------------------------------------	
def makeCommunitiesSubgraphs(G,partition):
	communities = {}
	for node in partition:
		community_no = partition[node]
		communities[community_no] = [node] if community_no not in communities else communities[community_no].append(node)
	
	for community_no in communities:
		nodes = communities[community_no]
		subGraph = G.subgraph(nodes)
		graphInfo(subGraph)

def convert_partition_in_dict_format(partition_fs):
	"""
	NetworkX returns partition object as an iterator, community module returns dictionary
	Function convert NetworkX partition object into a community partition dictaionary object
	"""
	partition = {}	
	for fs_no,fs in enumerate(partition_fs):
		community = list(fs)
		for v in community:
			partition[v] = fs_no
	return partition

def makeCommunities(graph,weight = True):
	"""
	Use Louvain Greedy Maximize to maximize Modularity
	"""
	partition = None
	if weight == True:
		partition = community.best_partition(graph, weight = 'weight')
	else:
		partition = community.best_partition(graph, weight = None)
	return partition

def makeGreedyCommunities(G,weight = True):
	"""
	Use Girvan Newman Algorithm to Maximize Modularity
	"""
	partition = None
	if weight == True:
		partition = nx.algorithms.community.modularity_max.greedy_modularity_communities(G,weight = "weight")
	else:
		partition =  nx.algorithms.community.modularity_max.greedy_modularity_communities(G,weight = None)
	return partition

def makeGNCommunity(graph):
	"""
	Use Girvan Newman Algorithm to Maximize Modularity
	"""
	partition = nx.algorithms.community.centrality.girvan_newman(graph)
	return partition

def makeASYN_LPACommunities(G,weight = True):
	"""
	Use Asynchronous Label Propogation to Maximize Modularity
	"""
	partition = None
	if weight == True:
		partition = nx.algorithms.community.label_propagation.asyn_lpa_communities(G, weight = "weight", seed = None)
	else:
		partition = nx.algorithms.community.label_propagation.asyn_lpa_communities(G, weight = None, seed = None)
	return partition

def makeLPACommunities(G,weight = True):
	"""
	Use Synchronous Label Propogation to Maximize Modularity
	"""
	partition = None
	if weight == True:
		partition = nx.algorithms.community.label_propagation.label_propagation_communities(G)
	else:
		partition = nx.algorithms.community.label_propagation.label_propagation_communities(G)
	return partition

def getCommunityPerformance(G,partition):
	"""
	Get Community Performance of the partition
	"""
	return nx.algorithms.community.quality.performance(G, partition)

def getCommunityCoverage(G,partition):
	"""
	Get Community Coverage of the partition
	"""
	return nx.algorithms.community.quality.coverage(G, partition)

def makeCommunityInducedGraph(graph,partition,weight = True):
	"""
	Get Community Induced Graph of the partition
	"""
	induced_subgraph = None
	if weight == True:
		induced_subgraph = community.induced_graph(partition,graph, weight = 'weight')
	else:
		induced_subgraph = community.induced_graph(partition,graph, weight = None)
	return induced_subgraph

def getModularity(graph,partition,weight = True):
	"""
	Get Modularity Value for the Partition
	"""
	modularity = None
	if weight ==  True:
		modularity = community.modularity(partition,graph,weight = "weight")
	else:
		modularity = community.modularity(partition,graph,weight = None)
	return modularity


def convert_to_Pajek(G,filename):
	"""
	Convert Graph into Pajek Format
	"""
	print("Writing In pajek Format to ",filename)
	nx.write_pajek(G,"Data/collusive_users_graph_Pajek.net",encoding = 'UTF-8')
	print("Written to Pajek")

#----------------------------------PajekFunctions------------------------------------------------

def convert_to_Pajek(G,filename):
	"""
	Convert Graph into Pajek Format
	"""
	print("Writing In pajek Format to ",filename)
	nx.write_pajek(G,filename,encoding = 'UTF-8')
	print("Written To",filename,"in Pajek Format")

def makePajekGraphIDtoNetworkXID(graphfilename):
	"""
	"""
	rows = basic_functions.openCSVfile(graphfilename,"	")
	PajekGraphID2NetworkxGraphID = {}
	for row in rows:
		if row[0] == "*edges":
			print("GOT edges")
			break
		if row[0] == "*vertices":
			print("GOT vertices")
			continue
		pajekGraphID = int(row[0])
		networkXGraphID = int(row[1])
		print(pajekGraphID,networkXGraphID)
		if pajekGraphID not in PajekGraphID2NetworkxGraphID:
			PajekGraphID2NetworkxGraphID[pajekGraphID] = networkXGraphID
		else:
			try:
				raise KeyboardInterrupt
			finally:
				print('Self-Defined Error:Duplicate Value Exception in makePajekGraphIDtoNetworkXID Function')
	return PajekGraphID2NetworkxGraphID

def get_Coreness(corefilename,PajekGraphID2NetworkxGraphID):
    rows = basic_functions.openCSVfile(corefilename,"	")
    rows = rows[1:]
    coreNessDictionary = {}
    for row_no,row in enumerate(rows):
        print(row_no,row)
        graphID = PajekGraphID2NetworkxGraphID[row_no + 1]
        WeightedCoreness = int(row[0])
        coreNessDictionary[graphID] = WeightedCoreness
    return coreNessDictionary

#------------------------------- K_CORE ---------------------
def makeKcore(graph,coreNessDictionary):
	degNodes = []
	peripheryNodes = []
	max_coreness = -1

	for vertex in coreNessDictionary:
		w_coreness = coreNessDictionary[vertex]
		if max_coreness < w_coreness:
			max_coreness = w_coreness

	print("Maximum Weighted Coreness = ",max_coreness)
	print("Found ")

	for vertex in coreNessDictionary:
		weightedCoreness = coreNessDictionary[vertex]
		if weightedCoreness >= max_coreness:
			degNodes.append(str(vertex))
		else:
			peripheryNodes.append(str(vertex))

	print("Making the Degerency Core....")
	degCore = graph.subgraph(degNodes)

	print("Making the Periphery Graph")
	peripheryGraph = graph.subgraph(peripheryNodes)
	return degCore,peripheryGraph


#------------------------------- Pajek as K_CORE ---------------------
def makeKcore(graph,coreNessDictionary):
    degNodes = []
    peripheryNodes = []
    max_coreness = -1
    
    for vertex in coreNessDictionary:
        w_coreness = coreNessDictionary[vertex]
        if max_coreness < w_coreness:
            max_coreness = w_coreness
    
    print("Maximum Weighted Coreness = ",max_coreness)
    print("Found ")
    
    for vertex in coreNessDictionary:
        weightedCoreness = coreNessDictionary[vertex]
        if weightedCoreness >= max_coreness:
            degNodes.append(str(vertex))
        else:
            peripheryNodes.append(str(vertex))
    
    print("Making the Degerency Core....")
    degCore = graph.subgraph(degNodes)
    
    print("Making the Periphery Graph")
    peripheryGraph = graph.subgraph(peripheryNodes)
    return degCore,peripheryGraph


#------------------------Centrality Functions--------------------------------------------------

def makeEigenVectorCentralityDict(graph,weight = False):
    eigenvector_cent= {}
    if weight == False:
        eigenvector_cent = nx.eigenvector_centrality(graph, max_iter = 100, tol = 1e-06, nstart = None,weight = None)
    else:
        eigenvector_cent = nx.eigenvector_centrality(graph, max_iter = 100, tol = 1e-06, nstart = None, weight = 'weight')
    return eigenvector_cent
    
def makePageRank(graph,weight = False):
    page_rank = []
    if weight == False:
        page_rank = nx.pagerank(graph, alpha = 0.85, personalization = None, max_iter = 100, tol = 1e-06, nstart = None, weight = None, dangling = None)
    else:
        page_rank = nx.pagerank(G, alpha = 0.85, personalization = None, max_iter = 100, tol=1e-06, nstart = None, weight = 'weight', dangling = None)
    return page_rank



#-----------------------------------------Make Degrees as a Dictionary-------------------------------------

def makeWeightedDegreeDictionary(graph):
    weighted_vertices = sorted(graph.degree(weight = "weight"), key = lambda x: x[1], reverse = True)
    WeightedDegreeDictionary = {}
    for vertex in weighted_vertices:
        WeightedDegreeDictionary[vertex[0]] = vertex[1]
    return WeightedDegreeDictionary
    
def makeDegreeDictionary(graph):
    vertices = sorted(graph.degree, key = lambda x: x[1], reverse = True)
    DegreeDictionary = {}
    for vertex in vertices:
        DegreeDictionary[vertex[0]] = vertex[1]
    return DegreeDictionary




#-----------------------------------------Normalize Dictionary------------------------------------

def normalizeDict(dictionary):
    maxValue = -1
    new_dictionary = {}
    for v in dictionary:
        value = dictionary[v]
        if value > maxValue:
            maxValue = value
    for v in dictionary:
        new_value = dictionary[v]/maxValue
        new_dictionary[v] = new_value
    return new_dictionary

#---------------------------------------------------------------------------------------------------------------------

def makeRandomWeightedGraph(n = 10,m = 10,weight_range = 10):
	G = nx.gnm_random_graph(n,m)
	for (u,v,w) in G.edges(data=True):
		w['weight'] = random.randint(0,weight_range)
	return G

def getAdjacencyMatrix(G,weighted  = True,format = "numpy"):
	adj = {}
	if weighted == True:
		adj = nx.adjacency_matrix(G, weight='weight')
	else:
		adj = nx.adjacency_matrix(G)
	if format == "numpy":
		return xn.to_numpy_matrix(adj)
	elif format == "dict":
		return to_dict_of_dicts(adj)
	elif format == "scipy":
		return to_scipy_sparse_matrix(adj)
	else:
		print("Invalid Format , returning in numpy format")
		return to_numpy_matrix(adj)


if __name__ == "__main__":
	pass