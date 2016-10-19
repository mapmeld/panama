# Panama

https://github.com/mapmeld/panama

This is a tutorial for using Neo4j with Web.PY server framework and real-world data from the Panama Papers.

There are four features of this project using Neo4j searches:

- generic search
- name search (with a regular expression helper)
- de-duping name search
- country search (uses more advanced graph features)

## Install

Make sure to install the Neo4j graph database (which requires Java Runtime Environment (JRE)).
You can use an installer with the Panama Papers data built in at https://offshoreleaks.icij.org/pages/database

If you want to quickly insert sample data, run ```sample-data.py``` in this folder.

Install Python and pip

Install the Python driver for Neo4j, ```pip install py2neo```

## Tutorial

Ideally you should have start with a demo of Neo4j web console at http://localhost:7474 and by changing
the default password. You can download the complete Panama Papers dataset at https://offshoreleaks.icij.org/pages/database

If you want to quickly insert sample data, run ```sample-data.py``` in this folder. If you retrieved the data separately, you will need to name its folder as graph.db inside ```/usr/local/Cellar/neo4j/*/libexec/data/databases/```

### Generic search

This is an example for connecting to the Neo4j database:

```python
# pip install py2neo
from py2neo import Graph, Node, Relationship

# connect to localhost:7474 to set your password
g = Graph(user="neo4j", password="admin")
```

Making a search:

```python
person = g.find_one("Officer", "name", searchQuery)
```

### Name search

We might know a first name or last name but not the full name, with matching capitalization, of the Panama
Papers record. A good example is the Icelandic PM who was made to resign. His name is written differently in Icelandic, the Panama Papers records, and the English-speaking press. This search allows us to look up several people at once.


#### De-duping names

Emma Watson appears in the dataset twice, because one record has her middle name and the other does not.

### Country search

#### Visualizing country search results

## License

Code is open source, MIT License

Written instructions are free under the Creative Commons Zero license
