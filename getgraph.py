''' Script to get nodes and edges from a repo.

    To use the script create a config file and then update a `config_file` 
    variable in the main() method.
    The config file contains a json file that contains the following properties:
    
{   "repoinput" :       "path to the target repo", 
    "reportoutput" :    "path to the directory to put put the CSV.",
    "blacklist":        "list of filenames to exclude." }

    5/26/2019 0.1.0
'''

import json
import os
import uuid
import datetime
import logging
import markdown
from bs4 import BeautifulSoup
import devrelutilities as DR

THISDATE = str(datetime.date.today())
STEM = "C:\Git\MS\\"
STEML = len(STEM)


def remove_items_from_repo(inlist, droplist):
    '''Takes a list and then drops items in the blacklist.'''
    outlist = []
    dropset = set(droplist)
    for i in inlist:
        filename = i.split("\\")[-1].split(".")[0].lower()
        if filename not in dropset:
            outlist.append(i)
    return outlist


def create_nodes_from_path(inrepo, inblacklist, node_dict):
    '''With the name of a repo a blacklist, and node dictionary, parses a 
    docs repo looking for target files and updates a dict of the nodes.
    node[path] = [path, "article", filename]'''
    try:
        files = DR.get_all_files(inrepo)
        docstoget = remove_items_from_repo(files, inblacklist)
    
        for i in docstoget:
            file, ext = os.path.splitext(i)
            ext = ext[1:] #trim the extension dot.
            path = i[STEML:] # trim the directory stem (C:\Git\MS\)
            filename = file.split("\\")[-1]
            include = i.find("include")
            media = i.find("media")
            if ext == "yml":
                pass #drop all yml files
            elif include > 0:
                node_dict[path] = [path, "include", filename]
            elif media > 0:
                node_dict[path] = [path, "media", filename]
            elif ext == "md":
                node_dict[path] = [path, "article", filename]

        return node_dict

    except Exception as e:
        logging.error("There was an issue with {}: {}.".format(infile, e))
        return node_dict


def get_edges_from_file(infile, edge):
    '''Take a path to mark downfile, extract links, and add to the edges'''
    try:
        filein = DR.get_text_from_file(infile)
        html_doc = markdown.markdown(filein)
        soup = BeautifulSoup(html_doc, 'html.parser')
        for link in soup.find_all('a'):
            link_body = link['href']
            if link_body[:4] == "http":
                link_type = "external"
            else:
                link_type = "internal"
            edge_id = str(uuid.uuid4())
            edge[edge_id] = [infile[STEML:], "link", link_body, link_type]
            logging.info("Created edge {}.".format(edge[edge_id]))
        return edge

    except Exception as e:
        logging.error("Issue getting links from: {}. Issue: {}.".format(infile, e))
        return edge


def create_edges_from_nodes(edges, nodes):
    '''With a dict of nodes, loop over the articles to extract links, and add to 
    the edges. Return edges'''
    for key, value in nodes.items():
        if value[1] == "article":
            path = STEM + key
            edges = get_edges_from_file(path, edges)
    return edges


def add_nodes_from_edges(edges, nodes):
    '''Take edges and nodes and if a targer in edges isn't a node, 
    add the node. Return nodes'''
    for value in edges.values():
        if value[2] in set(nodes.keys()):
            pass
        else:
            nodes[value[2]] = [value[2], "external", value[2]]
    return nodes


def main():
    '''Generate Neo4J files for importing into database.'''

    config_file = open(r"C:\Git\MB\devrelgraph\config.json")
    config_str = config_file.read()
    config = json.loads(config_str)
    path_in = config["repoinput"]
    path_out = config["reportoutput"]
    blacklist = config["blacklist"]
    
    print("Starting...") 
    OUTLOG = path_out + "graphloader-" + THISDATE + "-log.txt"
    logging.basicConfig(filename=OUTLOG, level=logging.INFO)
    logging.info("Starting.".format())
    nodes = {}
    edges = {}
    nodes = create_nodes_from_path(path_in, blacklist, nodes)
    edges = create_edges_from_nodes(edges, nodes)
    nodes = add_nodes_from_edges(edges, nodes)

    nodes_file = path_out + "nodefile.json"
    with open(nodes_file, 'w') as fp:
        json.dump(nodes, fp)

    edge_file = path_out + "edgefile.json"
    with open(edge_file, 'w') as fp:
        json.dump(edges, fp)

    print("Parsed {} nodes.".format(len(nodes)))
    print("Parsed {} edges.".format(len(edges)))
    logging.info("Done.".format())
    print("Done...") 

if __name__ == "__main__":
    main()
