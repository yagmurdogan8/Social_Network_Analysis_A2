import csv
import networkx as nx
# import io
import urllib.request

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

mentionGraph = nx.Graph()

for user, mentions in mentioned_users_list.items():
    for mentioned_user in mentions:
        if not mentionGraph.has_edge(user, mentioned_user):
            mentionGraph.add_edge(user, mentioned_user, weight=1)
        else:
            mentionGraph[user][mentioned_user]["weight"] += 1

# csv file for the edges
with open("weighted_edge_list.csv", mode='w', newline='', encoding="utf-8") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["Source", "Target", "Weight"])
    for edge in mentionGraph.edges(data=True):
        source, target, data = edge
        weight = data['weight']
        writer.writerow([source, target, weight])

print("Nodes: ", mentionGraph.nodes)
print("Edges: ", mentionGraph.edges)
print("Strongly connected components: ", nx.strongly_connected_components(mentionGraph))
print("Weakly connected components: ", nx.weakly_connected_components(mentionGraph))
print("Number of strongy connected components: ", len(nx.strongly_connected_components(mentionGraph)))
print("Number of weakly connected components: ", len(nx.weakly_connected_components(mentionGraph)))

