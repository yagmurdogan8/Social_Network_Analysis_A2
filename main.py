import csv
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

        # Print mentioned users for the current user
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

print("************ E N D     O F    Q U E S T I O N 1 ************")

# Q3.2
# nodes
print("Nodes: ", directedMentionGraph.nodes())
print("No of nodes: ", len(directedMentionGraph.nodes()))
# edges
print("Edges: ", directedMentionGraph.edges())
print("No of edges: ", len(directedMentionGraph.edges()))

# strongly connected comp
print("Strongly connected components: ", nx.strongly_connected_components(directedMentionGraph))
strongly_connected_components = list(nx.strongly_connected_components(directedMentionGraph))
print("Number of strongy connected components: ", len(strongly_connected_components))
for i, component in enumerate(strongly_connected_components):
    print("Size of strongly connected component ", i + 1, ": ", len(component))

# weakly connected comp
print("Weakly connected components: ", nx.weakly_connected_components(directedMentionGraph))
weakly_connected_components = list(nx.weakly_connected_components(directedMentionGraph))
print("Number of weakly connected components: ", len(weakly_connected_components))
# length is number of components but what is the difference between size and length?

# density = 2m/n.(n-1)
density = (2 * len(directedMentionGraph.edges())) / (len(directedMentionGraph.nodes()) * (len(directedMentionGraph.nodes()) - 1))
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

