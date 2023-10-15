import networkx as nx
import io
import urllib.request

# paring data from url
small_data_url = urllib.request.urlopen("https://liacs.leidenuniv.nl/~takesfw/SNACS/twitter-small.tsv")
large_data_url = urllib.request.urlopen("https://liacs.leidenuniv.nl/~takesfw/SNACS/twitter-larger.tsv")

small_data = small_data_url.read().decode('utf-8')
large_data_url = large_data_url.read().decode('utf-8')