""":START_ID,role,:END_ID,:TYPE
keanu,"Neo",tt0133093,ACTED_IN
laurence,"Morpheus",tt0133093,ACTED_IN
carrieanne,"Trinity",tt0234215,ACTED_IN

To load:

worked:
LOAD CSV FROM "http://MATTBRIGGS.US/mycdn/edgefile.csv" AS line
MERGE (n:A {filename : line.START_ID})
WITH line, n
MERGE (m:B {filename : line.END_ID})
WITH m,n
MERGE (n)-[:LINKS]->(m);

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