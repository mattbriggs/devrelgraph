import devrelutilities as DR
import json
import os

def main():    
    print("Starting")
    config_file = open(r"C:\Git\MB\Azure-Stack-Doc-Projects-Python\Dev-Rel-Graph\config.json")
    config_str = config_file.read()
    config = json.loads(config_str)
    path_in = config["repoinput"]
    path_out = config["reportoutput"]
    blacklist = ["toc", "index", "readme"]
    files = DR.get_all_files(path_in)
    nodes = [["filename", "type", "path"]]
    for i in files:
        file, ext = os.path.splitext(i)
        ext = ext[1:]
        path = i[9:]
        filename = file.split("\\")[-1]
        include = i.find("include")
        media = i.find("media")
        if ext == "yml":
            pass
        elif include > 0:
            nodes.append([filename, "include", path])
        elif media > 0:
            nodes.append([filename, "media", path])
        elif ext == "md":
            nodes.append([filename, ext, path])

    nodes_file = path_out + "nodefile.csv"
    DR.write_csv(nodes, nodes_file)


if __name__ == "__main__":
    main()