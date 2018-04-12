import json
from rdflib import Graph, Namespace, Literal, URIRef
import pycountry


def get_countries():
    f = open("playlists.json", "r")
    playlists = json.loads(f.read())
    f.close()
    f = open("songs.json", "r")
    songs = json.loads(f.read())
    f.close()
    country_graph = Graph()
    info_graph = Graph()
    dbo = Namespace("http://dbpedia.org/ontology/")
    dbp = Namespace("http://dbpedia.org/property/")
    mc = Namespace("http://localhost:3030/mc")
    for playlist in playlists["playlists"]:
        genres = []
        durations = []
        tracks = []
        popular_tracks = []
        popular_genres = []
        try:
            country = pycountry.countries.get(name=playlist["country"]).alpha_2
        except KeyError:
            try:
                country = pycountry.countries.get(common_name=playlist["country"]).alpha_2
            except KeyError:
                country = playlist["country"]
        print(playlist["country"])
        country_graph.load("http://dbpedia.org/resource/" + playlist["country"].replace(" ", "_"))

        for song in songs["songs"]:
            if song["country"] == country:
                for genre in song["genres"]:
                    already_added = False
                    for gen in genres:
                        if genre == gen:
                            already_added = True
                            gen["count"] += 1
                            break
                    if not already_added:
                        genres.append({"genre": genre, "count": 1})
                durations.append(song["duration"])

        if len(genres) > 5:
            for i in range(5):
                current_largest = genres[0]
                current_largest_index = 0
                counter = 0
                for genre_instance in genres:
                    if current_largest["count"] < genre_instance["count"]:
                       current_largest = genre_instance
                       current_largest_index = counter
                    counter += 1
                popular_genres.append(current_largest["genre"])
                genres[current_largest_index]["count"] = -1
        for s, p, o in country_graph.triples((None, dbo.populationDensity, None)):
            info_graph.add([s, p, o])
        for s, p, o in country_graph.triples((None, dbo.populationDensityRank, None)):
            info_graph.add([s, p, o])
        for s, p, o in country_graph.triples((None, dbp.gdpPpp, None)):
            info_graph.add([s, p, o])
        for s, p, o in country_graph.triples((None, dbp.gdpPppPerCapita, None)):
            info_graph.add([s, p, o])
        for s, p, o in country_graph.triples((None, dbp.gini, None)):
            info_graph.add([s, p, o])
        for s, p, o in country_graph.triples((None, dbp.hdi, None)):
            info_graph.add([s, p, o])
        for s, p, o in country_graph.triples((None, dbp.hdiRank, None)):
            info_graph.add([s, p, o])
        average_duration = sum(durations) / len(durations)
        country_node = URIRef("http://dbpedia.org/resource/" + playlist["country"].replace(" ", "_"))
        info_graph.add([country_node, mc.Duration, Literal(average_duration)])
        info_graph.add([country_node, mc.Code, Literal(country.lower())])
        for genre in popular_genres:
            info_graph.add([country_node, mc.Genre, Literal(genre)])
        for track in tracks:
            info_graph.add([country_node, mc.Song, Literal(track)])
    f = open("db.rdf", "w")
    f.write(str(info_graph.serialize()))
    f.close()


if __name__ == "__main__":
    get_countries()
