#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install py2neo
# connect to localhost:7474 to set your password
from py2neo import Graph, Node, Relationship
g = Graph(user="neo4j", password="admin")

artists = [
  {
    "name": "Pablo Picasso",
    "moma_id": 4609,
    "artworks": [
      {
        "name": "Meditation (Contemplation)",
        "moma_id": 33823,
        "date": "late 1904"
      },
      {
        "name": "Self Portrait (Yo)",
        "moma_id": 80026,
        "date": "late 1904"
      },
      {
        "name": "La belle qui passe",
        "moma_id": 36462,
        "date": "1904"
      },
      {
        "name": "Brooding Woman (recto), Three Children (verso)",
        "moma_id": 33008,
        "date": "1904"
      },
      {
        "name": "The Frugal Repast (Le repas frugal )",
        "moma_id": 73115,
        "date": "1904"
      }
    ]
  },
  {
    "name": "Francisco Borès",
    "moma_id": 678,
    "artworks": [
      {
        "name": "The Fitting",
        "moma_id": 78316,
        "date": "1934"
      }
    ]
  },
  {
    "name": "Marc Chagall",
    "moma_id": 1055,
    "artworks": [
      {
        "name": "Calvary",
        "moma_id": 79365,
        "date": "1912"
      },
      {
        "name": "Standing Nude",
        "moma_id": 36854,
        "date": "1904"
      },
      {
        "name": "I and the Village",
        "moma_id": 78984,
        "date": "1911"
      },
      {
        "name": "Vaslaw Nijinsky",
        "moma_id": 37234,
        "date": "1911"
      }
    ]
  }
]

def addArtist(artist, artwork):
    r = Node("Artwork", title=artwork["name"], date=artwork["date"], moma_id=artwork["moma_id"])
    tx.create(r)
    m = Relationship(artist, "ARTIST_OF", r, order=1)
    tx.create(m)

for artist in artists:
    tx = g.begin()
    activeArtist = Node("Artist", name=artist["name"], moma_id=artist["moma_id"])
    tx.create(activeArtist)
    
    for artwork in artist["artworks"]:
        addArtist(activeArtist, artwork)
    tx.commit()
