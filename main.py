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
                mentioned_user = word[1:]
                mentioned_users.append(mentioned_user)

        mentioned_users_list[username] = mentioned_users

        # Print mentioned users for the current user
        if mentioned_users:
            print(username, " mentioned: ", ", ".join(mentioned_users))

        print("-----------------------------------------------------")

    else:
        print("Tweet does not have tab spaces that I can split!!!")  # last line has a new line after it that's why i
        # added this
