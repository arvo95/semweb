import requests
import re
import json


def get_playlists():
    offset = 0
    pattern = re.compile("^The Needle / (?P<country>[A-Za-z\s]+)$")
    playlists = []
    headers = {"Authorization": "Bearer BQA-3t_IqzeYlpaQv5MJ0NyPn-fNRE1d9XRdD-wS7CHYTGcARYiJ4Ua9lsyiwAvzOO0j1VeiBB0bNIqoJyK65Agmh-6ZHLeP5Q5b4yiuU4iWr9JkQ9sw-ZhnmSxpUPm7pBkvmaugcIPVj970p6I5J_YdOXU4cx0"}
    for i in range(10):
        response = requests.get("https://api.spotify.com/v1/users/thesoundsofspotify/playlists?limit=50&offset=" + str(offset),
                                headers=headers)
        data = response.json()
        offset += 50
        for entry in data["items"]:
            if pattern.match(entry["name"]):
                playlists.append({"location": entry["href"], "country": re.match(pattern, entry["name"]).group("country")})
    f = open("playlists.json", "w")
    f.write(json.dumps({"playlists": playlists}))
    f.close()


if __name__ == "__main__":
    get_playlists()
