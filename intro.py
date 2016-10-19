# pip install py2neo
from py2neo import Graph, Node, Relationship

# connect to localhost:7474 to set your password
g = Graph(user="neo4j", password="admin")

# person = g.find_one("Artwork", "moma_id", workID)
# streetnames = g.run("MATCH (n:Street) WHERE {nodeid} IN n.nodeids RETURN n.nameslug LIMIT 25", nodeid=node)

