import argparse # argparse is a python package for CLI programming
import json
import http.client
from pathlib import Path
import sys
import climage
import urllib.request
import shutil
import tempfile
from urllib.parse import quote
import os

def lastfmPython():
    
    parser = argparse.ArgumentParser(description="A small Last.Fm search client written in python able to executed in terminal; Functions as a way for me to practice Python as beginner") # shorten func
    exclusive = parser.add_mutually_exclusive_group()

    exclusive.add_argument("--user", "-u", help="queries for a given user's info")
    exclusive.add_argument("--userRecentTracks", help="queries for a user's recent tracks")
    exclusive.add_argument("--userTopTracks", help="queries for a user's top tracks, time defaults to overall")
    exclusive.add_argument("--track", "-t", nargs=2, help="queries for a given track name and artist; use underscore for spaces")
    exclusive.add_argument("--toptracks", help="queries for the top tracks on lastfm", action="store_true")
    exclusive.add_argument("--topartists", help="queries for the top artists on lastfm", action="store_true")
    exclusive.add_argument("--album", "-a", nargs=2, help="queries for a given album name and artist; use underscore for spaces")
    exclusive.add_argument("--artist", nargs=1, help="queries for a given artist name; use underscore for spaces")
    parser.add_argument("-v", "--verbose", help="prints API key, HTTP info", action="store_true")

    parser.parse_args() # return previous arguments to python parser
    args = parser.parse_args() # make it even simpler

    key = ""

    file_name = "config.json"

    if os.path.exists(file_name) == False:
        with open(file_name, "w") as file:
            print("No config file found! Please setup your API key in the config file! It has been created in your local directory.")
            file.write('{"api_key": ""}') 
            sys.exit() 
    else:
        try: 
            with open(file_name, "r") as file:
                confJsonLoad = file.read()
                keyJson = json.loads(confJsonLoad)
                key = keyJson['api_key']
        except json.decoder.JSONDecodeError:
            print("No key found! Please setup your API key in the config file! It can be found in your local directory. Once you believe you are done, run lastfmPython -h")

    if args.user:
        user = args.user # get user prompt
        lastfmServer = http.client.HTTPSConnection("ws.audioscrobbler.com") 
        lastfmServer.request("GET", "/2.0/?method=user.getInfo&user=" + user + "&api_key=" + key + "&format=json")
        lastfmResponse = lastfmServer.getresponse()

        lastfmData = lastfmResponse.read()
        lastfmJson = json.loads(lastfmData)

        if args.verbose:
            print(lastfmResponse.status, lastfmResponse.reason)
            print(key)
            print()
        if 'error' in lastfmJson:
            error = lastfmJson['error']
            message = lastfmJson['message']
            print('There has been an error!')
            print(f'Error: {error}, {message}')
            sys.exit()

        lastfmCoverLink = lastfmJson["user"]["image"][2]["#text"]
        with urllib.request.urlopen(lastfmCoverLink) as response:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                shutil.copyfileobj(response, tmp_file)
        lastfmCoverImage = climage.convert(tmp_file.name, width=64)

        lastfmUser = lastfmJson['user']['name']
        lastfmPlaycount = lastfmJson['user']['playcount']
        lastfmUserURL = lastfmJson['user']['url']

        print()
        print("Request: User Info")
        print(f"User: {lastfmUser}")
        print(f"Playcount: {lastfmPlaycount}")
        print(f"URL: {lastfmUserURL}")
        print(lastfmCoverImage)
    elif args.userRecentTracks:
        user = args.userRecentTracks # get user prompt
        lastfmServer = http.client.HTTPSConnection("ws.audioscrobbler.com") 
        lastfmServer.request("GET", "/2.0/?method=User.getrecenttracks&user=" + user + "&api_key=" + key + "&format=json&limit=5")
        lastfmResponse = lastfmServer.getresponse()

        lastfmData = lastfmResponse.read()
        lastfmJson = json.loads(lastfmData)

        if args.verbose:
            print(lastfmResponse.status, lastfmResponse.reason)
            print(key)
            print()
        if 'error' in lastfmJson:
            error = lastfmJson['error']
            message = lastfmJson['message']
            print('There has been an error!')
            print(f'Error: {error}, {message}')
            sys.exit()
        
        lastfmUser = lastfmJson['recenttracks']['@attr']['user']

        print()
        print("Request: Recent Tracks")
        print(f"User: {lastfmUser}")
        print(f"Link: https://www.last.fm/user/{lastfmUser}")
    

        for track in range(5):
            print(f'{track + 1}. "{lastfmJson['recenttracks']['track'][track]['name']}" by {lastfmJson['recenttracks']['track'][track]['artist']['#text']}')
            print(f'   Played at: {lastfmJson['recenttracks']['track'][track]['date']['#text']}')
            print(f'   Link: {lastfmJson['recenttracks']['track'][track]['url']}')
    elif args.userTopTracks:
        user = args.userTopTracks # get user prompt
        lastfmServer = http.client.HTTPSConnection("ws.audioscrobbler.com") 
        lastfmServer.request("GET", "/2.0/?method=User.getTopTracks&user=" + user + "&api_key=" + key + "&format=json&limit=5")
        lastfmResponse = lastfmServer.getresponse()

        lastfmData = lastfmResponse.read()
        lastfmJson = json.loads(lastfmData)

        if args.verbose:
            print(lastfmResponse.status, lastfmResponse.reason)
            print(key)
            print()
        if 'error' in lastfmJson:
            error = lastfmJson['error']
            message = lastfmJson['message']
            print('There has been an error!')
            print(f'Error: {error}, {message}')
            sys.exit()

        lastfmUser = lastfmJson['toptracks']['@attr']['user']
        
        print()
        print("Request: User Top Tracks")
        print(f"User: {lastfmUser}")
        print(f"Link: https://www.last.fm/user/{lastfmUser}")

        for track in range(5):
            print(f'{track + 1}. "{lastfmJson['toptracks']['track'][track]['name']}" by {lastfmJson['toptracks']['track'][track]['artist']['name']}')
            print(f'   Plays: {lastfmJson['toptracks']['track'][track]['playcount']}')
            print(f'   Link: {lastfmJson['toptracks']['track'][track]['url']}')


    elif args.track:
        trackName = args.track[0] # get track name prompt
        trackNameConv = trackName.replace("_","%20")
        trackArtist = args.track[1] # get track artist prompt from 2nd arg
        trackArtistConv = trackArtist.replace("_","%20")
        lastfmServer = http.client.HTTPSConnection("ws.audioscrobbler.com") 
        lastfmServer.request("GET", f"/2.0/?method=track.getInfo&track={trackNameConv}&artist={trackArtistConv}&api_key={key}&format=json&autocorrect=1")
        lastfmResponse = lastfmServer.getresponse()

        lastfmData = lastfmResponse.read()
        lastfmJson = json.loads(lastfmData)

        if args.verbose:
            print(lastfmResponse.status, lastfmResponse.reason)
            print(key)
            print()
        if 'error' in lastfmJson:
            error = lastfmJson['error']
            message = lastfmJson['message']
            print('There has been an error!')
            print(f'Error: {error}, {message}')
            sys.exit()

        if "album" in lastfmJson["track"]:
            lastfmCoverLink = lastfmJson["track"]["album"]["image"][2]["#text"]
            with urllib.request.urlopen(lastfmCoverLink) as response:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    shutil.copyfileobj(response, tmp_file)
            lastfmCoverImage = climage.convert(tmp_file.name, width=64)
        
        print()
        print(f"Request: Track Info: '{trackName}' by {trackArtist}")

        print(f'Track Name: "{lastfmJson["track"]["name"]}"')
        trackNameConv2 = lastfmJson["track"]["name"].replace("_","+")
        print(f'Track Artist: {lastfmJson["track"]["artist"]["name"]}')
        trackArtistConv2 = lastfmJson["track"]["artist"]["name"].replace("_","+")
        if "wiki" in lastfmJson['track']:
            print(f'Track Published: {lastfmJson["track"]["wiki"]["published"]}')
        print(f"Link: https://www.last.fm/music/{trackArtistConv2}/_/{trackNameConv2}")
        if "album" in lastfmJson["track"]:
            print(f'Track Album: {lastfmJson["track"]["album"]["title"]}')
            print()
            print(lastfmCoverImage)

    elif args.album:
        albumName = args.album[0] # get track name prompt
        albumNameConv = albumName.replace("_", "%20")
        albumArtist = args.album[1] # get track artist prompt from 2nd arg
        albumArtistConv = albumArtist.replace("_","%20")
        lastfmServer = http.client.HTTPSConnection("ws.audioscrobbler.com") 
        lastfmServer.request("GET", f"/2.0/?method=album.getInfo&album={albumNameConv}&artist={albumArtistConv}&api_key={key}&format=json&autocorrect=1")
        lastfmResponse = lastfmServer.getresponse()

        lastfmData = lastfmResponse.read()
        lastfmJson = json.loads(lastfmData)

        if args.verbose:
            print(lastfmResponse.status, lastfmResponse.reason)
            print(key)
            print()
        if 'error' in lastfmJson:
            error = lastfmJson['error']
            message = lastfmJson['message']
            print('There has been an error!')
            print(f'Error: {error}, {message}')
            sys.exit()

        lastfmCoverLink = lastfmJson["album"]["image"][2]["#text"]
        with urllib.request.urlopen(lastfmCoverLink) as response:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                shutil.copyfileobj(response, tmp_file)
        lastfmCoverImage = climage.convert(tmp_file.name, width=64)
        
        print()
        print(f"Request: Album Info: '{albumName}' by {albumArtist}")

        print(f'Album Name: "{lastfmJson["album"]["name"]}"')
        albumNameConv2 = lastfmJson["album"]["name"].replace("_","+")
        print(f'Track Artist: {lastfmJson["album"]["artist"]}')
        albumArtistConv2 = lastfmJson["album"]["artist"].replace("_","+")
        print(f"Link: https://www.last.fm/music/{albumArtistConv2}/{albumNameConv2}")
        if "wiki" in lastfmJson['album']:
            print(f'Album Published: {lastfmJson["album"]["wiki"]["published"]}')
        if "image" in lastfmJson["album"]:
            print(lastfmCoverImage)

    elif args.artist:
        artistName = args.artist[0] # get track name prompt
        artistNameConv = artistName.replace("_", "%20")
        lastfmServer = http.client.HTTPSConnection("ws.audioscrobbler.com") 
        lastfmServer.request("GET", f"/2.0/?method=artist.getinfo&artist={artistNameConv}&api_key={key}&format=json&autocorrect=1")
        lastfmResponse = lastfmServer.getresponse()

        lastfmData = lastfmResponse.read()
        lastfmJson = json.loads(lastfmData)

        if args.verbose:
            print(lastfmResponse.status, lastfmResponse.reason)
            print(key)
            print()
        if 'error' in lastfmJson:
            error = lastfmJson['error']
            message = lastfmJson['message']
            print('There has been an error!')
            print(f'Error: {error}, {message}')
            sys.exit()

        lastfmCoverLink = lastfmJson["artist"]["image"][2]["#text"]
        with urllib.request.urlopen(lastfmCoverLink) as response:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                shutil.copyfileobj(response, tmp_file)
        lastfmCoverImage = climage.convert(tmp_file.name, width=64)
        
        print()
        print(f"Request: Artist Info: '{artistName}'")

        print(f'Album Name: "{lastfmJson["artist"]["name"]}"')
        artistNameConv2 = lastfmJson["artist"]["name"].replace("_","+")
        print(f"Link: https://www.last.fm/music/{artistNameConv2}")
        if "published" in lastfmJson['artist']['bio']:
            print(f'Page Published: {lastfmJson["artist"]["bio"]["published"]}')
        print()
        if "summary" in lastfmJson['artist']['bio']:
            print("Summary")
            print(lastfmJson['artist']['bio']['summary'])
            print()
        if "image" in lastfmJson["artist"]:
            print(lastfmCoverImage)

    elif args.toptracks:
        lastfmServer = http.client.HTTPSConnection("ws.audioscrobbler.com") 
        lastfmServer.request("GET", "/2.0/?method=chart.getTopTracks&api_key=" + key + "&format=json&limit=5")
        lastfmResponse = lastfmServer.getresponse()

        lastfmData = lastfmResponse.read()
        lastfmJson = json.loads(lastfmData)

        if args.verbose:
            print(lastfmResponse.status, lastfmResponse.reason)
            print(key)
            print()
        if 'error' in lastfmJson:
            error = lastfmJson['error']
            message = lastfmJson['message']
            print('There has been an error!')
            print(f'Error: {error}, {message}')
            sys.exit()

        print()
        print("Request: Top Tracks")

        for trackIndex in range(5):
            print(f'{trackIndex + 1}. "{lastfmJson["tracks"]["track"][trackIndex]["name"]}" by {lastfmJson["tracks"]["track"][trackIndex]["artist"]["name"]}')
            print(f"   Playcount: {lastfmJson["tracks"]["track"][trackIndex]["playcount"]}")
            print(f"   Link: {lastfmJson["tracks"]["track"][trackIndex]["url"]}")

    elif args.topartists:
        lastfmServer = http.client.HTTPSConnection("ws.audioscrobbler.com") 
        lastfmServer.request("GET", "/2.0/?method=chart.getTopArtists&api_key=" + key + "&format=json&limit=5")
        lastfmResponse = lastfmServer.getresponse()

        lastfmData = lastfmResponse.read()
        lastfmJson = json.loads(lastfmData)

        if args.verbose:
            print(lastfmResponse.status, lastfmResponse.reason)
            print(key)
            print()
        if 'error' in lastfmJson:
            error = lastfmJson['error']
            message = lastfmJson['message']
            print('There has been an error!')
            print(f'Error: {error}, {message}')
            sys.exit()

        print()
        print("Request: Top Artists")

        for artistIndex in range(5):
            print(f'{artistIndex + 1}. {lastfmJson["artists"]["artist"][artistIndex]["name"]}')
            print(f"   Playcount: {lastfmJson["artists"]["artist"][artistIndex]["playcount"]}")
            print(f"   Link: {lastfmJson["artists"]["artist"][artistIndex]["url"]}")