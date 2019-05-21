''' Script to get nodes from a repo.
    To use the script create a config file and then update a `config_file` variable in the main() method.
    The config file contains is a json file that contaains the following properties:
    
{   "repoinput" :       "path to the target repo", 
    "reportoutput" :    "path to the directory to put put the CSV.",
    "blacklsit":        "list of filenames to exclude." }

'''

import devrelutilities as DR
import json
import os


def remove_items(inlist, droplist):
    '''Takes a list and then drops items in the black list.'''
    outlist = []
    for i in inlist:
        check = i.lower()
        for j in droplist:
            if check.find(j) > 0:
                print("Dropped {}".format(i))
            else:
                outlist.append(i)
    return outlist

def create_nodes(inrepo, outpath, blacklist):
    '''With the name of a repo and a blacklist, parses a docs repo looking for target files and creates a table with the nodes.'''
    try:
        files = DR.get_all_files(inrepo)
        files_to_get = remove_items(files, blacklist)
    
        nodes = [["path", "type", "filename"]]
        for i in files_to_get:
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
                nodes.append([path, "media",filename])
            elif ext == "md":
                nodes.append([path,  ext, filename])

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
    
    print("Starting...:") 
    nodes = create_nodes(path_in, path_out, blacklist)
    nodes_file = outpath + "nodefile.csv"
    DR.write_csv(nodes, nodes_file)
    print("Saved {}".format(created))
    

if __name__ == "__main__":
    main()