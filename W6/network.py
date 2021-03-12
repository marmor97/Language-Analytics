''' Assignment description - Creating reusable network analysis pipeline
This exercise is building directly on the work we did in class. I want you to take the code we developed together and in you groups and turn it into a reusable command-line tool. This command-line tool will take a given dataset and perform simple network analysis. In particular, it will build networks based on entities appearing together in the same documents, like we did in class.
'''

# System tools
import os
import argparse # To make arguments from the terminal
from pathlib import Path

# Data analysis
import pandas as pd
from collections import Counter
from itertools import combinations 

# NLP
import spacy
nlp = spacy.load("en_core_web_sm")
import scipy

# drawing
import networkx as nx
# import pygraphviz
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,20)


class network_pipeline:
    def __init__(self, edgelist_name): # Always starting with "self" , weight_threshold
        # self.data_folder = data_folder # Assigning data folder to a self
        self.edgelist_name = edgelist_name
        
    def read_edgelist(self):
        root_dir = Path.cwd() # Path pastes the parent folder
        input_file = os.path.join(root_dir, self.edgelist_name) # Joining both root_dir, the data folder (defined above) and the image name also defined above
        edgelist = pd.read_csv(input_file)
        return edgelist
    
    # Function for making a network from the edgelist dataframe
    def make_network(self, counted_edgelist, threshold):
        filtered = counted_edgelist[counted_edgelist["weights"] > threshold]
        network = nx.from_pandas_edgelist(filtered, 'nodeA', 'nodeB', ["weights"])
        return network
    
    def plot_network(self, network, path_to_save, filename):
        # Plotting and saving the image 
        outpath_viz = os.path.join(path_to_save, filename)
        pos = nx.drawing.nx_pylab.draw_spring(network,node_size=5, with_labels=False)
        nx.draw(network, pos, with_labels=True, node_size=20, font_size=5)
        plt.savefig(outpath_viz, dpi=300, bbox_inches="tight")
        
    def calc_measures(self, network, path_to_save, filename):
        ev = nx.eigenvector_centrality(network)
        bc = nx.betweenness_centrality(network)
        d = pd.DataFrame({'eigenvector':ev, 'betweenness':bc})
        outpath_vals = os.path.join(path_to_save, filename)
        d.to_csv(outpath_vals,index=False)
   
        
def main(): # Now I'm defining the main function where I try to make it possible executing arguments from the terminal
    # add description
    ap = argparse.ArgumentParser(description = "[INFO] creating network pipeline") # Defining an argument parse

    ap.add_argument("-e","--edgelist_name", 
                    required=False, # As I have provided a default name it is not required
                    type = str, # Str type
                    default = "data/edgelist.csv", # Setting default to the name of my own edgelist
                    help = "str of edgelist filename")
    
    ap.add_argument("-w","--weight_treshold", 
                    required=False, # As I have provided a default name it is not required
                    type = int, # Str type
                    default = 500, # Setting default to the name of my own edgelist
                    help = "int of threshold weights")
    
    args = vars(ap.parse_args()) # Adding them together
    
    network_generation = network_pipeline(edgelist_name = args["edgelist_name"]) # Defining what they corresponds to in the network pipeline class and functions
    threshold = args["weight_treshold"]
    # Using the above defined data folder and edgelist name to read the edgelists
    counted_edgelist = network_generation.read_edgelist()
    # Taking the make_network function to make a network
    network = network_generation.make_network(counted_edgelist, threshold)
    # Plot network
    network_generation.plot_network(network, "viz", "network.png")
    # Calculate betweenness and eigenvector centrality
    network_generation.calc_measures(network, "output", "network_measures.csv")
    
if __name__ == "__main__":
    main()
         