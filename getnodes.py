''' Script to get nodes from a repo.
    To use the script create a config file and then update a `config_file` variable in the main() method.
    The config file contains is a json file that contaains the following properties:
    
{   "repoinput" :       "path to the target repo", 
    "reportoutput" :    "path to the directory to put put the CSV.",
    "blacklist":        "list of filenames to exclude." }

'''

import devrelutilities as DR
import json
import os


def remove_items_from_repo(inlist, droplist):
    '''Takes a list and then drops items in the blacklist.'''
    outlist = []
    dropset = set(droplist)
    for i in inlist:
        filename = i.split("\\")[-1].split(".")[0].lower()
        print(filename)
        if filename not in dropset:
            outlist.append(i)
    return outlist


def create_nodes(inrepo, inblacklist):
    '''With the name of a repo and a blacklist, parses a docs repo looking for target files and creates a table with the nodes.'''
    try:
        files = DR.get_all_files(inrepo)
        docstoget = remove_items_from_repo(files, inblacklist)
    
        nodes = [["path", "type", "filename"]]
        for i in docstoget:
            file, ext = os.path.splitext(i)
            ext = ext[1:] #trim the extension dot.
            path = i[9:] # trim the directory stem (C:\Git\MS\)
            filename = file.split("\\")[-1]
            include = i.find("include")
            media = i.find("media")
            if ext == "yml":
                pass
            elif include > 0:
                nodes.append([path, "include", filename])
            elif media > 0:
                nodes.append([path, "media", filename])
            elif ext == "md":
                nodes.append([path, "article", filename])

        return nodes

    except Exception as e:
        print("There was an issue: {}".format(e))
        return [[]]


def main():
    '''Generate Neo4J files for importing into database.'''

    config_file = open(r"C:\Git\MB\devrelgraph\config.json")
    config_str = config_file.read()
    config = json.loads(config_str)
    path_in = config["repoinput"]
    path_out = config["reportoutput"]
    blacklist = config["blacklist"]
    
    print("Starting...") 
    doc_nodes = create_nodes(path_in, blacklist)
    nodes_file = path_out + "nodefile.csv"
    DR.write_csv(doc_nodes, nodes_file)
    print("Saved {}".format(nodes_file))


if __name__ == "__main__":
    main()