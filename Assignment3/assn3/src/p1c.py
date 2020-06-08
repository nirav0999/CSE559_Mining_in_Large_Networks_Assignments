import networkx as nx
import basic_functions
import graph_functions
import matplotlib.pyplot as plt
import copy
import math

#The last digits of the node_id initially votes for
A_voted_by = [4,5,6,7]
B_voted_by = [0,1,2,3]
Undecided = [8,9]

#Changes the default global variable deciding an Undecided Candidate's votes
def change_Advantage(adv):
	adv = "A" if adv == "B" else "B"
	return adv

# Make a distribution of the dictionary
def make_distribution(dictionary):
	distribution = {}
	for v in dictionary:
		val = dictionary[v]
		if val in distribution:
			distribution[val].append(v) 
		else:
			distribution[val] = [v]
	return distribution

# Iniialize the votes
def votes_for(node_id,votes):
	vote = int(str(node_id)[-1])
	if vote in A_voted_by:
		votes[node_id] = "A"
	elif vote in B_voted_by:
		votes[node_id] = "B" 
	else:
		votes[node_id] = "U"
	return votes

# This is done so that nodes with the same degree appear in advertising array in ascending order
def sort_again(sorted_nodes):	
	popularity_dict = {}
	for v in sorted_nodes:
		node_id = int(v[0])
		popularity = v[1]
		if popularity in popularity_dict:
			popularity_dict[popularity].append(v)
		else:
			popularity_dict[popularity] = [v]

	for p in popularity_dict:
		arr = popularity_dict[p]
		arr.sort()
		popularity_dict[p] = arr

	pop_values = list(popularity_dict.keys())
	pop_values.sort(reverse = True)

	final_sorted_nodes = []

	for v in pop_values:
		arr = popularity_dict[v]
		for node in arr:
			final_sorted_nodes.append(node)

	return final_sorted_nodes



def make_Advertising_Group(graph,amount):

	nfpeople_reached = amount//10000

	#Sorting the nodes by Degree in decreasing order
	sorted_nodes = graph_functions.sortNodesByDegree(graph,weight = None,reverse = True)
	#print(sorted_nodes[:10])
	sorted_nodes = sort_again(sorted_nodes)
	#print(sorted_nodes[:10])
	advertised_to = []

	for i in range(nfpeople_reached):
		advertised_to.append(sorted_nodes[i][0])
	return advertised_to


def advertise(group,votes,change_to):
	for person in group:
		#print("Changing ",person[0],"from",votes[person[0]],"to","A")
		votes[person] = change_to
	return votes

def make_graph(filename):
	G = nx.Graph()
	rows = basic_functions.openCSVfile(filename," ")
	Votes = {}
	for row in rows:
		node1_id = int(row[0])
		node2_id = int(row[1])
		G.add_edge(node1_id,node2_id)
		Votes = votes_for(node1_id,Votes)
		Votes = votes_for(node2_id,Votes)
	print(graph_functions.graphInfo(G,0,False,False,False))
	return G,Votes

def determine_result(final_votes):
	vote_distribution = make_distribution(final_votes)
	assert len(list(vote_distribution.keys())) == 2
	#print(vote_distribution.keys())
	nfVotesA = len(vote_distribution["A"])
	nfVotesB = len(vote_distribution["B"])

	if nfVotesA > nfVotesB:
		return "A",nfVotesA - nfVotesB
	elif nfVotesA < nfVotesB:
		return "B",nfVotesB - nfVotesA
	else:
		return "U",0

def simulate_election(G,nf_days,init_votes,advantage_candidate):
	dist_votes = make_distribution(init_votes)
	
	init_undecided_voters = copy.deepcopy(dist_votes["U"])
	init_undecided_voters.sort()
	
	current_votes = copy.deepcopy(init_votes)

	for iter_no in range(nf_days):

		for voter in init_undecided_voters:	
			
			# print("Undecided Voter = ",voter)

			nf_A_neighbor_voters = 0
			nf_B_neighbor_voters = 0
			nf_U_neighbor_voters = 0

			for neighbhor in G.neighbors(voter):

				if current_votes[neighbhor] == "A":
					nf_A_neighbor_voters += 1
				elif current_votes[neighbhor] == "B":
					nf_B_neighbor_voters += 1
				elif current_votes[neighbhor] == "U":
					nf_U_neighbor_voters += 1


			if nf_A_neighbor_voters > nf_B_neighbor_voters:
				current_votes[voter] = "A"
			elif nf_A_neighbor_voters < nf_B_neighbor_voters:
				current_votes[voter] = "B"
			else:
				current_votes[voter] = advantage_candidate
				#print("Changing Advantage Candidate........")
				#print("Prev advantage_candidate = ",advantage_candidate)
				advantage_candidate = change_Advantage(advantage_candidate)
				#print("New advantage_candidate = ",advantage_candidate)


		#advantage_candidate = change_Advantage(advantage_candidate)

	return current_votes



def advertise_before_simulate(G,amount,nf_days,init_votes,advantage_candidate,title = ""):
	margin_won = []
	amounts_spend = []
	min_margin = math.inf
	ideal_amount = math.inf

	for k in range(0,amount+1,1000):

		advertise_to = make_Advertising_Group(G,k)
		init_votes1 = advertise(advertise_to,init_votes,"A")
		final_votes = simulate_election(G,nf_days = 7,init_votes = init_votes1,advantage_candidate = advantage_candidate)
		winner,margin = determine_result(final_votes)
		
		#print("The election was won by",winner,"with a margin of",margin,"amount spend",k)
		
		if winner == "B":
			margin =  -1 * margin

		if winner == "A":
			#print(margin)
			if margin < min_margin:
				min_margin = margin
				ideal_amount = k

		
		margin_won.append(margin)
		amounts_spend.append(k)


	plt.plot(amounts_spend,margin_won)
	plt.xlabel("Amount Spend")
	plt.ylabel("Margin of Victory")
	plt.xticks([0,10000,20000,30000,40000,50000,60000,70000,80000,90000])
	plt.title(title)
	plt.show()

	return 	min_margin,ideal_amount


Adv_Candidate = "A"

G1,Init_Votes1 = make_graph("../q1-data/g1.edgelist.txt")
G2,Init_Votes2 = make_graph("../q1-data/g2.edgelist.txt")

print("------------------------------SOCIAL GRAPH 1-----------------------------------")
min_margin,ideal_amount = advertise_before_simulate(G1,amount = 90000,nf_days = 7,init_votes = Init_Votes1,advantage_candidate = Adv_Candidate,title = "G1 Social graph")
print("The minimum amount of money that needs to be spent by A is ",ideal_amount,"winning by",min_margin)
print("------------------------------SOCIAL GRAPH 2-----------------------------------")
min_margin,ideal_amount = advertise_before_simulate(G2,amount = 90000,nf_days = 7,init_votes = Init_Votes2,advantage_candidate = Adv_Candidate,title = "G2 Social graph")
print("The minimum amount of money that needs to be spent by A is ",ideal_amount,"winning by",min_margin)





	




