import networkx as nx
import basic_functions
import graph_functions
import copy

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

#Make the graph
def make_graph(filename):
	G = nx.Graph()
	rows = basic_functions.openCSVfile(filename," ")
	Votes = {}
	
	for row in rows:

		#Node ID's assigned 
		node1_id = int(row[0])
		node2_id = int(row[1])
		
		#Add an edge in the graph
		G.add_edge(node1_id,node2_id)

		#Assign Votes to the nodes
		Votes = votes_for(node1_id,Votes)
		Votes = votes_for(node2_id,Votes)

	#Print the basic information of the graph
	print(graph_functions.graphInfo(G,0,False,False,False))

	return G,Votes


#Determine the result of the election by counting the votes
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
		return "U"

def simulate_election(G,nf_days,init_votes,advantage_candidate):
	
	#Make the distribution of votes
	dist_votes = make_distribution(init_votes)
	
	#Initial Undecided Voters
	init_undecided_voters = dist_votes["U"]

	#Soritng the undecided Voters by voter_id
	init_undecided_voters.sort()
	
	current_votes = copy.deepcopy(init_votes)

	for iter_no in range(nf_days):

		for voter in init_undecided_voters:	
			
			# print("Undecided Voter = ",voter)

			nf_A_neighbor_voters = 0
			nf_B_neighbor_voters = 0
			nf_U_neighbor_voters = 0


			#Calculate the #Votes for each campaign and the undecided voters
			for neighbhor in G.neighbors(voter):

				if current_votes[neighbhor] == "A":
					nf_A_neighbor_voters += 1
				elif current_votes[neighbhor] == "B":
					nf_B_neighbor_voters += 1
				elif current_votes[neighbhor] == "U":
					nf_U_neighbor_voters += 1

			# Assign the final vote of the campaign
			if nf_A_neighbor_voters > nf_B_neighbor_voters:
				current_votes[voter] = "A"
			elif nf_A_neighbor_voters < nf_B_neighbor_voters:
				current_votes[voter] = "B"
			else:
				#Assign the candidate 
				current_votes[voter] = advantage_candidate
				print("Changing Advantage Candidate........")
				print("Prev advantage_candidate = ",advantage_candidate)

				#Changing the Advantage Candidate
				advantage_candidate = change_Advantage(advantage_candidate)
				print("New advantage_candidate = ",advantage_candidate)

	return current_votes




Adv_Candidate = "A"


#Making  the graphs
G1,Init_Votes1 = make_graph("../q1-data/g1.edgelist.txt")
G2,Init_Votes2 = make_graph("../q1-data/g2.edgelist.txt")


#print(Init_Votes1)

# for v in Init_Votes1:
# 	print(v,Init_Votes1[v])


#Final Vote tallies of the winners
final_votes1 = simulate_election(G1,nf_days = 7,init_votes = Init_Votes1,advantage_candidate = Adv_Candidate)
final_votes2 = simulate_election(G2,nf_days = 7,init_votes = Init_Votes2,advantage_candidate = Adv_Candidate)


winner,margin = determine_result(final_votes1)
print("For graph G1 ,The election was won by",winner,"with a margin of",margin)

winner,margin = determine_result(final_votes2)
print("For graph G2 ,The election was won by",winner,"with a margin of",margin)




	




