''' Script to get nodes from a repo.
    To use the script create a config file and then update a `config_file` variable in the main() method.
    The config file contains a json file that contains the following properties:
    
{   "repoinput" :       "path to the target repo", 
    "reportoutput" :    "path to the directory to put put the CSV.",
    "blacklist":        "list of filenames to exclude." }

    The output of this script will be used by the getedges script.
'''

import devrelutilities as DR
import json
import os
import csv
import json
import markdown
from bs4 import BeautifulSoup

class Graph:
    pass

class Node:
    pass

class Edge:
    pass

class Utility:
    pass

