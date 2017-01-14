import requests
import unicodedata
import json
import spotipy
sp = spotipy.Spotify()
import spotipy.util as util
from functions import *
from bs4 import BeautifulSoup as bs4
from row import Row
import datetime
import dateutil.parser
import ckua_web as ckua
from secret import SPOTIFY_SECRET

CLIENT_ID = 'beee62c8844a49b48128f4fbc83ba723'
CLIENT_SECRET = SPOTIFY_SECRET
REDIRECT_URI = 'http://localhost:3000'
username = 'ckua'

uris = []

# january playlist
playlist_id = '54neuNjfHiHUG26FuWjpDB'

# TODO: set date properly
today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)
offset = 7
offset_day = today - datetime.timedelta(days = offset)
remove_age = 7
remove_day = today - datetime.timedelta(days = remove_age)

# this json includes all of the schedule information, and relates each show to its playlist
with open('schedule.json') as f:
    schedule = json.load(f)

# the scopes requested
scope = 'playlist-modify-public'
# spotify authentication
token = util.prompt_for_user_token('ckua',client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri = REDIRECT_URI, scope=scope)


if token:
    sp = spotipy.Spotify(auth=token)
    # this section removes tracks that are past their expiry date
    for program in schedule['shows']:
        if 'uri' in program:
            uri = program['uri']
            # get a list of all tracks in playlist
            size_res = sp.user_playlist_tracks(username, playlist_id = uri, fields='total')
            size = int(size_res['total'])
            remove_list = []
            # establish the expiry date
            playlist_remove_day = today - datetime.timedelta(days = program['lifespan'])

            # spotify only returns 100 items, so 'a is used to keep track of the offset
            for a in range(0, size/100 + 1):

                playlist = sp.user_playlist_tracks(username, playlist_id = uri, offset = str(100*a), fields='total, items(added_at, track(name, uri))')
                for index, item in enumerate(playlist['items']):
                    day = dateutil.parser.parse(item['added_at'])
                    # add to the list of tracks to be removed if it is older than the expiry date
                    if day.date() <= playlist_remove_day:
                        rem = {"uri": item['track']['uri'] , "positions" : [100*a + index]}
                        remove_list.append(rem)

            print remove_list

            # break it into groups of 100
            rem_chunks = list(chunks(remove_list, 100))
            rem_chunks.reverse()
            for chunk in rem_chunks:
                # spotipy remove the tracks
                sp.user_playlist_remove_specific_occurrences_of_tracks(username, playlist_id = uri, tracks = chunk)

    # this section adds tracks to the playlists
    # this is the range of days we will look at on the CKUA website
    # 1 = yesterday
    # range goes from the first parameter to the day before the second parameter
    # so range(1,2) will do yesterday only
    for offset in range(1, 2):

        offset_day = today - datetime.timedelta(days = offset)
        print offset_day
        print int_to_day(offset_day.weekday())
        url = "http://www.ckua.com/features/playlist?date=" + str(offset_day)

        # get the web page
        rows = ckua.get_ckua_tracks(url)

        # searches spotify for the tracks
        uris = get_uris(rows)

        # move uris into lists of 100 tracks
        chunk_list = list(chunks(uris, 100))

        if schedule:
            programs = find_program(rows, int_to_day(offset_day.weekday()), schedule)
            for key, value in programs.iteritems():
                chunk_list = list(chunks(value, 100))
                for i in chunk_list:
                    # adds the tracks in groups of 100 or less to the playlists
                    sp.user_playlist_add_tracks(username, key, i)


else:
    print "Can't get token"
