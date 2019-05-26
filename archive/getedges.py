"""
Script creates a CSV that contains the following columns from links.

:START_ID","asset",":END_ID",":TYPE

Steps:
1. Check that you have a configuration file `config.json` that contains a 
JSON object the following attributes: { "repoinput" : "path to the target repo", 
"reportoutput" : "output directory" }
2. In the main() routine the config.json is loaded. Check the path.
2.  Check that you have the output CSV of the getnodes.py script. The script gets
the CSV, and then loops over each 'article' node, retrieves the links, and then
builds the output CSV.
3. Run the script.

"""

import os
import csv
import json
import markdown
from bs4 import BeautifulSoup
import devrelutilities as DR

STEM = "C:\Git\MS\\"


def get_links(infile, edges):
    '''Take a path to mark downfile, extract links, and add to the edge'''
    try:
        filein = DR.get_text_from_file(infile)
        html_doc = markdown.markdown(filein)
        soup = BeautifulSoup(html_doc, 'html.parser')
        for link in soup.find_all('a'):
            link_body = link['href']
            if link_body[:4] == "http":
                link_type = "link-external"
            else:
                link_type = "link-internal"
            edges.append([infile[len(STEM):], "link", link_body, link_type])
        return edges

    except Exception as e:
        print("Issue getting links from: {}. Issue: {}.".format(infile, e))
        return edges


def main():
    '''Generate Neo4J edges (relationships) for importing into database.'''

    config_file = open(r"C:\Git\MB\devrelgraph\config.json")
    config_str = config_file.read()
    config = json.loads(config_str)
    path_in = config["repoinput"]
    path_out = config["reportoutput"]
    
    print("Starting...") 
    csv_in = path_out + "nodefile.csv"
    readit = open(csv_in)
    nodes = csv.reader(readit)
    article_path = []
    for ext, i in enumerate(nodes):
        if ext > 0:
            if i[1] == "article":
                article_path.append(STEM + i[0])  # add the the directory stem
    edges = [[":START_ID","asset",":END_ID",":TYPE"]]
    for f in article_path:
        edges = get_links(f, edges)

    edge_file = path_out + "edgefile.csv"
    DR.write_csv(edges, edge_file)
    print("Saved {}".format(edge_file))


if __name__ == "__main__":
    main()