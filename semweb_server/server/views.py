# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rdflib import Graph, Namespace, Literal, URIRef
from django.http import JsonResponse


def fetch_country(request, country):
    country_graph = Graph()
    dbo = Namespace("http://dbpedia.org/ontology/")
    dbp = Namespace("http://dbpedia.org/property/")
    mc = Namespace("https://storage.googleapis.com/song_country_ontology/MC.ttl")
    country_graph.load("http://localhost:3030/songs", format="n3")
    genres = []
    response = {}

    for s, p, o in country_graph.triples((None, None, Literal(country.lower()))):
        for s2, p2, o2 in country_graph.triples((s, None, None)):
            if p2 == URIRef("http://localhost:3030/mcGenre"):
                genres.append(o2)
            elif p2 == dbo.populationDensity:
                response["populationDensity"] = o2
            elif p2 == dbo.populationDensityRank:
                response["populationDensityRank"] = o2
            elif p2 == dbp.gdpPpp:
                response["gdp"] = o2
            elif p2 == dbp.gdpPppPerCapita:
                response["gdpPerCapita"] = o2
            elif p2 == dbp.gini:
                response["gini"] = o2
            elif p2 == dbp.hdi:
                response["hdi"] = o2
            elif p2 == dbp.hdiRank:
                response["hdiRank"] = o2
            elif p2 == URIRef("http://localhost:3030/mcCode"):
                response["code"] = o2
            elif p2 == URIRef("http://localhost:3030/mcDuration"):
                response["duration"] = o2
        response["genres"] = genres
    return JsonResponse(response)
