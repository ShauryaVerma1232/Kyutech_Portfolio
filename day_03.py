# writing the deterministic model for the LLM to prioritse fixes in rememdiation 
nodes = ["node1", "node2", "node3"]
blast_score = [0.8, 0.6, 0.9]
mapping_score = {}
for i in range(len(nodes)):
    mapping_score[nodes[i]] = blast_score[i]

#unpacking mapping_score to get the blast score for each node
for node, score in mapping_score.items():
    sort_mapping_score = print(node, score)

# sorting mapping score in descending order
sorted_mapping_score = sorted(mapping_score.items(), key=lambda x: x[1], reverse=True)
print(sorted_mapping_score)
# full pckaged logic for rememdiation prioritisation
# def prioritize_remediation(nodes, blast_radius_scores):
#     mapping_score = {}
#     for i in range(len(nodes)):
#         mapping_score[nodes[i]] = blast_radius_scores[i]
    
#     sorted_nodes = sorted(mapping_score.items(), key=lambda x: x[1], reverse=True)
#     return sorted_nodes 