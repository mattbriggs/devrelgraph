'''With the output of the getgraph module, create two cypher files to load the data.'''

import json
import devrelutilities as DR


def def_make_alpha(number):
    letters = "abcdefghijklmnopqrstuvwxyz"
    outstring = ""
    instring = str(number)
    while len(instring) > 0:
        outstring += letters[int(instring[0])]
        instring = instring[1:]
    return outstring


def main():
    '''Generate Cypher from the output of the getgraph.py script.'''

    node_file = open(r"C:\data\nodefile.json")
    node_str = node_file.read()
    nodes = json.loads(node_str)
    edge_file = open(r"C:\data\edgefile.json")
    edge_str = edge_file.read()
    edges = json.loads(edge_str)

    node_cypher = ""
    for indx, value in enumerate(nodes.values()):
        a = def_make_alpha(indx)
        node_cypher += 'CREATE ({}:Doc {{filename : "{}", doctype : "{}", path : "{}" }})\n'.format(a, value[2], value[1], value[0])
    node_cypher += ""
    edge_cypher = ""
    for indx, value in enumerate(edges.values()):
        a = "a" + def_make_alpha(indx)
        b = "b" + def_make_alpha(indx)
        r = "r" + def_make_alpha(indx)
        edge_cypher += 'MATCH ({}:Doc) Where {}.path = "{}", Match ({}:Doc) Where {}.path = "{}" CREATE ({})-[{}:LINKS]->({})\n'.format(a, a, value[0], b, b, value[2], a, r, b)
    edge_cypher += ""

    DR.write_text(node_cypher, "C:\\data\\node-cypher.cql")
    DR.write_text(edge_cypher, "C:\\data\\edge-cypher.cql")

if __name__ == "__main__":
    main()
