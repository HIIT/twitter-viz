import tweepy
from keys import *
import networkx as nx
import matplotlib.pyplot as plt

auth = tweepy.OAuthHandler(keys[0], keys[1])
auth.set_access_token(keys[2], keys[3])

G=nx.Graph()

edge_colors = []
node_colors =[]

def myAddNode(tweetsauthor):
    
    if not G.has_node(tweetsauthor):
        node_colors.append('r')

    G.add_node(tweetsauthor)


def myAddEdge(tweetsauthor, mention):
    if not G.has_edge(tweetsauthor, mention):
        edge_colors.append('black')
    if not G.has_node(mention):
        node_colors.append('r')
    G.add_edge(tweetsauthor, mention, weight=10)

def myHashtagConnector(tweetsauthor, myHashtag):
    if not G.has_edge(tweetsauthor, myHashtag):
        edge_colors.append('b')
    if not G.has_node(myHashtag):
        node_colors.append('b')
    G.add_edge(tweetsauthor, myHashtag, weight=10)



class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print "author: "+status.author.screen_name
        
        plt.clf()

        myAddNode("user: "+status.author.screen_name)

        for elem in status.entities['user_mentions']:
            print "mention: "+elem['screen_name']
            myAddEdge('user: '+status.author.screen_name, "user: "+elem['screen_name'])

        for elem in status.entities['hashtags']:
            print "hashtag: "+elem['text']
            myHashtagConnector("user: "+status.author.screen_name, "hash: "+elem['text'])

        nx.draw_spring(G, node_size=25, edge_color=edge_colors, node_color=node_colors)#, with_labels=True)

        plt.savefig("map.png")




api = tweepy.API(auth)

myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener )

myStream.filter(track=['#digivaalit'])
