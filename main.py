import csv
import random
import networkx as nx
import urllib.request
import matplotlib.pyplot as plt

# Q3.1

# parsing data from url
small_data_url = urllib.request.urlopen("https://liacs.leidenuniv.nl/~takesfw/SNACS/twitter-small.tsv")
large_data_url = urllib.request.urlopen("https://liacs.leidenuniv.nl/~takesfw/SNACS/twitter-larger.tsv")

small_data = small_data_url.read().decode('utf-8')  # str
large_data = large_data_url.read().decode('utf-8')

lines = small_data.split('\n')
mentioned_users_list = {}

for index, line in enumerate(lines):  # burada index almada sorun yasadim enum eklemek zorunda kaldim.

    parts = line.strip().split('\t')
    if len(parts) >= 3:

        date, username, tweet = parts[0], parts[1], parts[2]

        print("Line no: ", index + 1)
        print("Date: ", date)
        print("Username: ", username)
        print("Tweet: ", tweet)

        words = tweet.split()
        mentioned_users = []

        for word in words:
            if word.startswith("@"):
                mentioned_user = word[1:]  # It did not work really, some of the nodes still has @ at beginning
                mentioned_users.append(mentioned_user)

        mentioned_users_list[username] = mentioned_users

        # print mentioned users for the current user
        if mentioned_users:
            print(username, " mentioned: ", ", ".join(mentioned_users))
            print(len(mentioned_users))

        print("-----------------------------------------------------")

    else:
        print("Line no: ", index + 1, "Tweet does not have tab spaces that I can split!!!")
        # last line has a new line after it that's why i added this
directedMentionGraph = nx.DiGraph()

for user, mentions in mentioned_users_list.items():
    for mentioned_user in mentions:
        if not directedMentionGraph.has_edge(user, mentioned_user):
            directedMentionGraph.add_edge(user, mentioned_user, weight=1)
        else:
            directedMentionGraph[user][mentioned_user]["weight"] += 1

# csv file for the edges
with open("weighted_edge_list.csv", mode='w', newline='', encoding="utf-8") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["Source", "Target", "Weight"])
    for edge in directedMentionGraph.edges(data=True):
        source, target, data = edge
        weight = data['weight']
        writer.writerow([source, target, weight])

print("\n************ E N D     O F    Q U E S T I O N 1 ************")

# Q3.2
# nodes
# print("Nodes: ", directedMentionGraph.nodes())
print("No of nodes: ", len(directedMentionGraph.nodes()))
# edges
# print("Edges: ", directedMentionGraph.edges())
print("No of edges: ", len(directedMentionGraph.edges()))

# strongly connected comp
print("Strongly connected components: ", nx.strongly_connected_components(directedMentionGraph))
strongly_connected_components = list(nx.strongly_connected_components(directedMentionGraph))
print("Number of strongy connected components: ", len(strongly_connected_components))

for i, component in enumerate(strongly_connected_components):
    print("Size of ", i + 1, ". strongly connected component : ", len(component))

# weakly connected comp
print("Weakly connected components: ", nx.weakly_connected_components(directedMentionGraph))
weakly_connected_components = list(nx.weakly_connected_components(directedMentionGraph))
print("Number of weakly connected components: ", len(weakly_connected_components))

for i, component in enumerate(strongly_connected_components):
    print("Size of ", i + 1, ". weakly connected component : ", len(component))

# density = 2m/n.(n-1)
density = (2 * len(directedMentionGraph.edges())) / (
        len(directedMentionGraph.nodes()) * (len(directedMentionGraph.nodes()) - 1))
print("Density of the network: ", density)

# indegree and outdegree distributions
indegree = dict(directedMentionGraph.in_degree())
outdegree = dict(directedMentionGraph.out_degree())

plt.hist(list(indegree.values()), bins=20, color='r')
plt.title('Indegree Distribution')
plt.xlabel('Indegree')
plt.ylabel('Frequency')
plt.show()

plt.hist(list(outdegree.values()), bins=20, color='r')
plt.title('Outdegree Distribution')
plt.xlabel('Outdegree')
plt.ylabel('Frequency')
plt.show()

# average cc directed & undirected
directed_average_clustering_coefficient = nx.average_clustering(directedMentionGraph)
print("Directed average clustering coefficint: ", directed_average_clustering_coefficient)

undirectedMentionGraph = directedMentionGraph.to_undirected()
undirected_average_clustering_coefficient = nx.average_clustering(undirectedMentionGraph)
print("Undirected average clustering coefficient: ", undirected_average_clustering_coefficient)

subset_size = 1000
all_nodes = list(undirectedMentionGraph.nodes())

subsets = []
for i in range(0, len(all_nodes), subset_size):
    subset_nodes = all_nodes[i:i + subset_size]
    subset_graph = undirectedMentionGraph.subgraph(subset_nodes)
    subsets.append(subset_graph)

giant_components_sub = []
avg_distance_list = []
avg_value = 0
for subset in subsets:
    connected_components = list(nx.connected_components(subset))
    if connected_components:
        giant_component = max(connected_components, key=len)
        giant_components_sub.append(subset.subgraph(giant_component))

for i, giant_component in enumerate(giant_components_sub):
    average_distance = nx.average_shortest_path_length(giant_component)
    avg_value += average_distance
    avg_distance_list.append(average_distance)

print("Average Distance in giant component: ", avg_value / len(avg_distance_list))

giant_component = max(nx.connected_components(undirectedMentionGraph), key=len)
giant_subgraph = undirectedMentionGraph.subgraph(giant_component)

sample_size = 50  # no of nodes as a sample
distance_distribution = {}

sample_nodes = random.sample(giant_subgraph.nodes(), sample_size)

for source_node in sample_nodes:
    distances = nx.single_source_shortest_path_length(giant_subgraph, source_node)

    for distance in distances.values():
        if distance in distance_distribution:
            distance_distribution[distance] += 1

total_counts = sum(distance_distribution.values())
distance_distribution = {distance: count / total_counts for distance, count in distance_distribution.items()}

plt.hist(list(distance_distribution.values()), bins=20, color='r')
plt.title('Distance Distribution of the Giant component')
plt.xlabel('Distance')
plt.ylabel('Frequency')
plt.show()

print("\n************ E N D     O F    Q U E S T I O N 2 ************")

# Q3.3

# # betweenness centrality - it takes ages
# # burasi hic calismiyor
# between_centrality = nx.betweenness_centrality(directedMentionGraph)
# edge_between_centrality = nx.edge_betweenness_centrality(undirectedMentionGraph)

# i = 0
# while i < 20:
#     top_between_node = max(between_centrality, key=between_centrality.get)
#     top_between_value = between_centrality.pop(top_between_node)
#     print((i + 1), ". user's name: @", top_between_node, " - value: ", top_between_value)
#     i += 1

# for i in range(20):
#     top_between_node = max(between_centrality, key=between_centrality.get)
#     top_between_value = between_centrality[top_between_node]
#     top_mentions.append(top_between_node)
#     print((i + 1), ". user's name: @", top_between_node, " - value: ", top_between_value)
#     del between_centrality[top_between_node]

top_mentions = []

# eigen vector centrality

ei_centrality = nx.eigenvector_centrality(undirectedMentionGraph)
direct_ei_centrality = nx.eigenvector_centrality(directedMentionGraph)

print("\n Top 20 mentions - with Eigen Vector Centrality (Undirected Graph) : \n")

i = 0
while i < 20:
    top_ei_node = max(ei_centrality, key=ei_centrality.get)
    top_ei_value = ei_centrality.pop(top_ei_node)
    print((i + 1), ". user's name: @", top_ei_node, " - value: ", top_ei_value)
    i += 1

print("\n Top 20 mentions - with Eigen Vector Centrality (Directed Graph) : \n")

i = 0
while i < 20:
    top_dei_node = max(direct_ei_centrality, key=direct_ei_centrality.get)
    top_dei_value = direct_ei_centrality.pop(top_dei_node)
    print((i + 1), ". user's name: @", top_dei_node, " - value: ", top_dei_value)
    i += 1

# closeness centrality
# ucloseness_centrality = nx.closeness_centrality(undirectedMentionGraph)
# undirected olunca calismiyo
# directedsa da ini var outu var

print("\n Top 20 mentions - with Closeness Centrality (Undirected graph): \n")

ucloseness_centrality = nx.closeness_centrality(undirectedMentionGraph)

for i in range(20):
    top_ucloseness_node = max(ucloseness_centrality, key=ucloseness_centrality.get)
    top_ucloseness_value = ucloseness_centrality[top_ucloseness_node]
    if top_ucloseness_node not in top_mentions:
        top_mentions.append(top_ucloseness_node)
        print((i + 1), ". user's name: @", top_ucloseness_node, " - value: ", top_ucloseness_value)
        del ucloseness_centrality[top_ucloseness_node]


print("\n Top 20 mentions - with Closeness Centrality (In degree): \n")

dcloseness_centrality = nx.closeness_centrality(directedMentionGraph, distance='in')

for i in range(20):
    top_closeness_node = max(dcloseness_centrality, key=dcloseness_centrality.get)
    top_closeness_value = dcloseness_centrality[top_closeness_node]
    if top_closeness_node not in top_mentions:
        top_mentions.append(top_closeness_node)
        print((i + 1), ". user's name: @", top_closeness_node, " - value: ", top_closeness_value)
        del dcloseness_centrality[top_closeness_node]

print("\n Top 20 mentions - with Closeness Centrality (Out degree): \n")

doutcloseness_centrality = nx.closeness_centrality(directedMentionGraph, distance='out')

for i in range(20):
    top_outcloseness_node = max(doutcloseness_centrality, key=doutcloseness_centrality.get)
    top_outcloseness_value = doutcloseness_centrality[top_outcloseness_node]
    if top_outcloseness_node not in top_mentions:
        top_mentions.append(top_outcloseness_node)
        print((i + 1), ". user's name: @", top_outcloseness_node, " - value: ", top_outcloseness_value)
        del doutcloseness_centrality[top_outcloseness_node]

# degree centarlity

degree_centrality = nx.degree_centrality(undirectedMentionGraph)  # bu yonden bagimsizmis
in_degree_centrality = nx.in_degree_centrality(directedMentionGraph)
out_degree_centrality = nx.out_degree_centrality(directedMentionGraph)

print("\n Top 20 mentions - with Degree Centrality (Undirected Graph): \n")

for i in range(20):
    top_degree_node = max(degree_centrality, key=degree_centrality.get)
    top_degree_value = degree_centrality[top_degree_node]
    top_mentions.append(top_degree_node)
    print((i + 1), ". user's name: @", top_degree_node, " - value: ", top_degree_value)
    del degree_centrality[top_degree_node]

print("\n Top 20 mentions - with Degree Centrality (In Degree): \n")

for i in range(20):
    top_indegree_node = max(in_degree_centrality, key=in_degree_centrality.get)
    top_indegree_value = in_degree_centrality[top_indegree_node]
    top_mentions.append(top_indegree_node)
    print((i + 1), ". user's name: @", top_indegree_node, " - value: ", top_indegree_value)
    del in_degree_centrality[top_indegree_node]

print("\n Top 20 mentions - with Degree Centrality (Out Degree): \n")

for i in range(20):
    top_outdegree_node = max(out_degree_centrality, key=out_degree_centrality.get)
    top_outdegree_value = out_degree_centrality[top_outdegree_node]
    top_mentions.append(top_outdegree_node)
    print((i + 1), ". user's name: @", top_outdegree_node, " - value: ", top_outdegree_value)
    del out_degree_centrality[top_outdegree_node]

print("\n************ E N D     O F    Q U E S T I O N 3 ************")

# Q3.4

# Louvain Algorithm

print("\n************ E N D     O F    Q U E S T I O N 4 ************")

# Q3.6

print("\n************ E N D     O F    Q U E S T I O N 6 ************")

# Q3.7
