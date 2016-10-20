# Panama

https://github.com/mapmeld/panama

This is a tutorial for using Neo4j with Web.PY server framework and real-world data from the Panama Papers
and Bahamas Leaks (updated October 2016).

This data was published by the International Consortium of Investigative Journalists. It is legal for
foreigners to have businesses and accounts in Panama, but the data includes several politicians and other
public figures who did not declare these investments or are avoiding taxes.

There are four features of this project using Neo4j searches:

- generic search
- name search (with a regular expression helper)
- de-duping name search
- country search (uses more advanced graph features)

## Install

Make sure to install the Neo4j graph database (which requires Java Runtime Environment (JRE)).
Even if you installed Neo4j before, you should use an installer with the Panama Papers data built in at https://offshoreleaks.icij.org/pages/database or run ```sample-data.py``` in this folder.

Install Python and pip

Install the Python driver for Neo4j, ```pip install py2neo```

## Tutorial

Ideally you should have start with a demo of Neo4j web console at http://localhost:7474 and by changing
the default password.

If you want to quickly insert sample data, run ```sample-data.py``` in this folder.

### Generic search

This is an example for connecting to the Neo4j database:

```python
# pip install py2neo
from py2neo import Graph, Node, Relationship

# connect to localhost:7474 to set your password
g = Graph(user="neo4j", password="admin")
```

Making a search returning one exact name match:

```python
searchQuery = web.input().search
person = g.find_one("Officer", "name", searchQuery)
return json.dumps(person)
```

### Name search

We might know a first name or last name, but not the full name, with matching capitalization, of the Panama
Papers record. A good example is the Icelandic PM who was made to resign. His full name is written differently in Icelandic, records, and some English-speaking press.

* Press: Sigmundur Gunnlaugsson
* Wikipedia: Sigmundur Davíð Gunnlaugsson
* Panama Papers: Sigmundur David Gunnlaugsson

This search also allows us to look up several people at once.

```python
# make a regular expression
# 'Sigmundur' -> '(?i).*Sigmundur.*'
# 'Emma Watson' -> '(?i).*Emma.*Watson.*'
searchQuery = web.input().search.strip()
searchQuery = '(?i).*' + searchQuery.replace(' ', '.*') + '.*'

# use =~ to compare to the regular expression
results = g.run("MATCH (p:Officer) WHERE p.name =~ {name} RETURN p", name=searchQuery)
people = []
for person in results:
    # each result contains an array [p]
    people.append(person[0])
return json.dumps(people)
```

#### De-duping names

Some people (including Emma Watson) have multiple records in the dataset, making it more difficult to map
out all of the connections.

The International Consortium of Investigative Journalists has added several 'SIMILAR_NAME_AND_ADDRESS_AS' relationships between other nodes, so that would be the first step to de-dupe records. This relationship was not added to Emma Watson's records, possibly because one record has her middle names
and the other does not.

In your future system, you could build a model to assist in this process... there is an especially useful Python project <a href="https://github.com/datamade/dedupe">DeDupe</a> which takes in training data and runs the model to filter your remaining data.

In this case, I'll focus on the SIMILAR_NAME_AND_ADDRESS_AS relation:

```python
query = """MATCH (p:Officer) WHERE p.name =~ {name}
  OPTIONAL MATCH (mainalt) -[:SIMILAR_NAME_AND_ADDRESS_AS]-> (p)
  OPTIONAL MATCH (p) -[:SIMILAR_NAME_AND_ADDRESS_AS]-> (alt)
  RETURN p, alt, mainalt"""
results = g.run(query, name=searchQuery)
people = []
for person in results:
    if person[2] is not None:
        continue
    people.append(person)
```

I tried to add ```WHERE mainalt IS null``` but it didn't work well.

Then adding in first/last name check:

```python
for person in results:
    if person[2] is not None:
        continue
    multinames = person[0]['name'].lower().split(' ')
    firstlast = multinames[0] + ' ' + multinames[len(multinames) - 1]
    if firstlast in names:
        # add as an alt to the previous record
        people[names.index(firstlast)][1] = person[0]
        continue
    else:
        names.append(firstlast)
    # add as an array like this because person is a Record object and cannot be reset later
    people.append([person[0], person[1], person[2]])
```

### Country graph search

'Countries' is an array property of the Officer object. We can return people who are from Mongolia and their direct entities like this:

```
MATCH (n:Officer { countries: 'Mongolia' }) MATCH (n) -[r]- (e:Entity) RETURN n, r, e
```

This is similar to a single JOIN query and returns some useful data. But how can we keep traversing the
graph and pick up more connections?

Here we use a new relationship to search for relationships in both directions

```
MATCH (n:Officer { countries: 'Mongolia' })
MATCH (n) -[*1..2]- (e)
RETURN n, e
```

Unfortunately one of our Mongolia-labeled Officers JOHN F BARGHUSEN, is a shareholder of ACCELONIC LTD. [Blue Earth Refineries Inc. (ex-NATURE EXTRAC LIMITED)]. There are around 1,000 known shareholders in the Panama Papers dataset, so expanding the query out another link would return all of their thousands of relationships, and the query stalls.  But I double checked and John is in Minnesota (abbreviation MN
was mistaken for Mongolia).  I deleted that record and was able to run the query. But if we try to go deeper on the whole dataset, we will reach more super-nodes.

But even with this number of queries, we can see a handful clusters, and one of them is the biggest.
CORPORATE MANAGEMENT SERVICES LIMITED has 23 related entities connected to 21 (de-duped) people based in Mongolia.

#### Visualizing country search results

## License

Code is open source, MIT License

Written instructions are free under the Creative Commons Zero license
