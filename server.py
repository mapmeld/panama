# pip install web.py py2neo
# connect to localhost:7474 to set your password
from py2neo import Graph, Node, Relationship
g = Graph(user="neo4j", password="admin")

import web
render = web.template.render('templates/')

import json

urls = (
  '/', 'home',
  '/person', 'person',
  '/bootstrap.min.css', 'bootstrap'
)

class home:
    def GET(self):
        return render.home()

class person:
    def GET(self):
        # simple query, no regex or dedupe
        searchQuery = web.input().search
        person = g.find_one("Officer", "name", searchQuery)
        # return json.dumps(person)

        # multiple with regexp
        searchQuery = searchQuery.replace(' ', '.*')
        results = g.run("MATCH (p:Officer) WHERE p.name =~ {name} RETURN p", name=searchQuery)
        people = []
        for person in results:
            people.append(person)
        return json.dumps(people)


class bootstrap:
    def GET(self):
        f = open('static/bootstrap.min.css', 'r')
        content = f.read()
        f.close()
        return content

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
