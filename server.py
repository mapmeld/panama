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
  '/place', 'place',
  '/bootstrap.min.css', 'bootstrap'
)

class home:
    def GET(self):
        return render.home()

class person:
    def GET(self):
        # (1) simple query, no regex or dedupe
        # searchQuery = web.input().search
        # person = g.find_one("Officer", "name", searchQuery)
        # return json.dumps(person)

        # (2) multiple results, with regexp
        # searchQuery = web.input().search
        # searchQuery = '(?i).*' + searchQuery.replace(' ', '.*') + '.*'
        # results = g.run("""MATCH (p:Officer)
        #   WHERE p.name =~ {name}
        #   RETURN p""", name=searchQuery)
        # people = []
        # for person in results:
        #     people.append(person[0])
        # return json.dumps(people)

        # (3) remove marked duplicates
        # searchQuery = web.input().search
        # searchQuery = '(?i).*' + searchQuery.replace(' ', '.*') + '.*'
        # query = """MATCH (p:Officer) WHERE p.name =~ {name}
        #   OPTIONAL MATCH (mainalt) -[:SIMILAR_NAME_AND_ADDRESS_AS]-> (p)
        #   OPTIONAL MATCH (p) -[:SIMILAR_NAME_AND_ADDRESS_AS]-> (alt)
        #   RETURN p, alt, mainalt"""
        # results = g.run(query, name=searchQuery)
        # people = []
        # for person in results:
        #     if person[2] is not None:
        #         continue
        #     people.append(person)
        # return json.dumps(people)

        # (4) remove first/last matches
        searchQuery = web.input().search
        searchQuery = '(?i).*' + searchQuery.replace(' ', '.*') + '.*'
        query = """MATCH (p:Officer) WHERE p.name =~ {name}
          OPTIONAL MATCH (mainalt) -[:SIMILAR_NAME_AND_ADDRESS_AS]-> (p)
          OPTIONAL MATCH (p) -[:SIMILAR_NAME_AND_ADDRESS_AS]-> (alt)
          RETURN p, alt, mainalt"""
        results = g.run(query, name=searchQuery)
        people = []
        names = []
        for person in results:
            if person[2] is not None:
                continue
            multinames = person[0]['name'].lower().split(' ')
            first_last_country = multinames[0] + ' ' + multinames[len(multinames) - 1] + ' ' + person[0]['countries']
            if first_last_country in names:
                people[names.index(first_last_country)][1] = person[0]
                continue
            else:
                names.append(first_last_country)
            people.append([person[0], person[1], person[2]])
        return json.dumps(people)

class place:
    def GET(self):
        searchQuery = web.input().search.strip()
        query = """MATCH (n:Officer { countries: {country} })
          MATCH (n) -[r]-> (e:Entity)
          RETURN n, r, e"""
        results = g.run(query, country=searchQuery)
        people = []
        for result in results:
            people.append([result[0], result[1].type(), result[2]])
        return render.results(people=people)

class bootstrap:
    def GET(self):
        f = open('static/bootstrap.min.css', 'r')
        content = f.read()
        f.close()
        return content

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
