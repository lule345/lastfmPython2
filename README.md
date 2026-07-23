# lastfm-python
A small Last.Fm search client written in python able to executed in terminal; Functions as a way for me to practice Python as beginner

```
options:
  -h, --help                                show this help message and exit
  --user, -u [user]                         queries for a given user's info
  --userRecentTracks [user]                 queries for a user's recent tracks
  --userTopTracks [user]                    queries for a user's top tracks, time defaults to overall
  --track, -t [name] [artist]               queries for a given track name and artist; use underscore for spaces
  --toptracks                               queries for the top tracks on lastfm
  --topartists                              queries for the top artists on lastfm
  --album, -a [name] [artist]               queries for a given album name and artist; use underscore for spaces
  --artist [artist]                         queries for a given artist name; use underscore for spaces
  -v, --verbose                             prints API key, HTTP info
```

- Supply your own Last.Fm API Key (see: https://www.last.fm/api/account/create)
- Licensed under GNU General Public License v3
- Available at PIP: https://pypi.org/project/PIP-lastfm-python-lule345/1.0.0/

![screenshot demo of lastfm.py](/screenshot1.png)