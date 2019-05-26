# Document Graph

Hackathon project for graph  database of docs that was started at Write the Docs 2019 in Portland.

# Overview

This is a set of small scripts that will crawl and parse a markdown repository in order to create a graph of related documents, media files, and off site URLs.

The two main scripts are:

| Script | Input | Output | Desscription |
| --- | --- | --- | --- | --- |
| getgraph.py | markdown repo | node.json<br>edge.json | This script parses the markdown to create a set of nodes from articles, media files, and external locations. |
| createcypher.py | node.json<br>edge.json | node.cql<br>edge.cql | This script prepares the JSON files as Cypher files to be ingested by Neo4j. |

# Get started

You will need to use a Neo4J database. You can find out more about Neo4J at: https://neo4j.com/lp/try-neo4j-sandbox/


# Use the scripts

1. Donwload and clone this repo.
2. Get or fresh the target markdown repo.
3. Create or update a config.json file.
    ```json  
    {   "repoinput" :       "path to the target repo", 
        "reportoutput" :    "path to the directory to output the JSON.",
        "blacklist":        "list of filenames to exclude." }
    ```

4. Run `getgraph.py` (This will produce two files node and edges in json)
5. Run `createcypher.py` (This will produce two files, cypher files for nodes and edges).
6. Open the Neo4J Database at http://your-ip:7474 and then type your username and password.
7. Clear the existing database.
    ```cypher
    MATCH (n) Delete (n)
    ```
8. Load the cypher files directly into the database or drag and drop them into the import panel.

9. Get the entire network.
    ```cypher
    match (n) return (n)
    ```

    ![Noe4J database](/media/graph.png)

10.  Get the links to a single mode. Find a value to grab the node. In this case I'm using a file path.
    ```cypher
    MATCH (a:Doc {path: 'azure-docs-cli\\docs-ref-conceptual\\get-started-with-azure-cli.md'})-[r]-(n) RETURN a, n
    ```

![Cypher queries in the database](/media/singlenode.png)

11. For more information on Cypher queries see [Cypher Basics](https://neo4j.com/developer/cypher-query-language/).

# Thanks