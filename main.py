import networkx as nx
# import io
import urllib.request

# parsing data from url
small_data_url = urllib.request.urlopen("https://liacs.leidenuniv.nl/~takesfw/SNACS/twitter-small.tsv")
large_data_url = urllib.request.urlopen("https://liacs.leidenuniv.nl/~takesfw/SNACS/twitter-larger.tsv")

small_data = small_data_url.read().decode('utf-8')  #str
large_data = large_data_url.read().decode('utf-8')

lines = small_data.split('\n')

for index, line in enumerate(lines):

    parts = line.strip().split('\t')
    if len(parts) >= 3:

        date, username, tweet = parts[0], parts[1], parts[2]

        print("Line no: ", index + 1)
        print("Date: ", date)
        print("Username: ", username)
        print("Tweet: ", tweet)
        print("-----------------------------------------------------")
    else:
        print("Tweet does not have tab spaces that I can split!!!")  # last line has a new line after it that's why i
        # added this

    # mentioned_users_list = {}
    #
    # for users in username:
    #     for mention in tweet:
    #         if mention.startswith('@'):
    #             mention = mention[1:]  # for getting only the username without at
    #             mentioned_users_list.keys().add(mention)
