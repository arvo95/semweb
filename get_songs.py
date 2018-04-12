import requests
import json
import pycountry


def get_songs():
    f = open("playlists.json", "r")
    playlists = json.loads(f.read())
    f.close()
    songs = []
    counter = 0
    headers = {"Authorization": "Bearer BQA-3t_IqzeYlpaQv5MJ0NyPn-fNRE1d9XRdD-wS7CHYTGcARYiJ4Ua9lsyiwAvzOO0j1VeiBB0bNIqoJyK65Agmh-6ZHLeP5Q5b4yiuU4iWr9JkQ9sw-ZhnmSxpUPm7pBkvmaugcIPVj970p6I5J_YdOXU4cx0"}
    for playlist in playlists["playlists"]:
        try:
            country = pycountry.countries.get(name=playlist["country"]).alpha_2
        except KeyError:
            try:
                country = pycountry.countries.get(common_name=playlist["country"]).alpha_2
            except KeyError:
                country = playlist["country"]
        response = requests.get(playlist["location"] + "/tracks?offset=0&limit=50", headers=headers)
        tracks = response.json()
        while True:
            for track in tracks["items"]:
                album = requests.get(track["track"]["album"]["href"], headers=headers)
                album_json = album.json()
                genres = []
                if album_json["genres"] == []:
                    for artist in track["track"]["album"]["artists"]:
                        artist = requests.get(artist["href"], headers=headers)
                        artist_json = artist.json()
                        genres += artist_json["genres"]
                else:
                    genres = album_json["genres"]
                songs.append({"name": track["track"]["name"], "genres": genres, "country": country, "popularity": track["track"]["popularity"],
                              "duration": track["track"]["duration_ms"], "release_date": album_json["release_date"],
                              "release_date_precision": album_json["release_date_precision"]})
            if tracks["next"] is None:
                break
            response = requests.get(tracks["next"], headers=headers)
            tracks = response.json()
        counter += 1
        print(str(counter) + " / " + str(len(playlists["playlists"])))
    print("Got " + str(len(songs)) + " songs.")
    f = open("songs.json", "w")
    f.write(json.dumps({"songs": songs}))
    f.close()


if __name__ == "__main__":
    get_songs()
