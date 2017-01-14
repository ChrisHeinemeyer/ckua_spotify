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
import math
CLIENT_ID = 'beee62c8844a49b48128f4fbc83ba723'
CLIENT_SECRET = '3d3c446958b54431ba8c4dc9b4a8d8cc'
REDIRECT_URI = 'http://localhost:3000'
username = 'ckua'
# ckua 2
playlist_id = '7wSU1Mf1AWj71ZESoce3Hp'

# # ckua
# playlist_id = '1qRTTWQk9AnQzoPc9UDnDL'
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

with open('schedule.json') as f:
    schedule = json.load(f)


scope = 'playlist-modify-public'
token = util.prompt_for_user_token('ckua',client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri = REDIRECT_URI, scope=scope)


if token:
    sp = spotipy.Spotify(auth=token)
    # get a list of all tracks in playlist
    size_res = sp.user_playlist_tracks(username, playlist_id = playlist_id, fields='total')


    size = int(size_res['total'])
    remove_list = []
    for a in range(0, size/100 + 1):

        playlist = sp.user_playlist_tracks(username, playlist_id = playlist_id, offset = str(100*a), fields='total, items(added_at, track(name, uri))')
        for index, item in enumerate(playlist['items']):
            day = dateutil.parser.parse(item['added_at'])
            if day.date() < remove_day:
                rem = {"uri": item['track']['uri'] , "positions" : [100*a + index]}
                remove_list.append(rem)


    rem_chunks = list(chunks(remove_list, 100))
    rem_chunks.reverse()
    for chunk in rem_chunks:
        sp.user_playlist_remove_specific_occurrences_of_tracks(username, playlist_id = playlist_id, tracks = chunk)
    # print pl

    for program in schedule['shows']:
        # get a list of all tracks in playlist
        if 'uri' in program:
            uri = program['uri']
            size_res = sp.user_playlist_tracks(username, playlist_id = uri, fields='total')
            size = int(size_res['total'])
            remove_list = []
            playlist_remove_day = today - datetime.timedelta(days = program['lifespan'])
            for a in range(0, size/100 + 1):

                playlist = sp.user_playlist_tracks(username, playlist_id = uri, offset = str(100*a), fields='total, items(added_at, track(name, uri))')
                for index, item in enumerate(playlist['items']):
                    day = dateutil.parser.parse(item['added_at'])
                    # print day
                    # print playlist_remove_day
                    if day.date() <= playlist_remove_day:
                        rem = {"uri": item['track']['uri'] , "positions" : [100*a + index]}
                        remove_list.append(rem)

            print remove_list
            rem_chunks = list(chunks(remove_list, 100))
            rem_chunks.reverse()
            for chunk in rem_chunks:
                sp.user_playlist_remove_specific_occurrences_of_tracks(username, playlist_id = uri, tracks = chunk)
        # print pl

    for offset in range(1, 2):

        offset_day = today - datetime.timedelta(days = offset)
        print offset_day
        print int_to_day(offset_day.weekday())
        url = "http://www.ckua.com/features/playlist?date=" + str(offset_day)
        # get the web page
        rows = ckua.get_ckua_tracks(url)


        uris = get_uris(rows)
        # move uris into lists of 100 tracks
        chunk_list = list(chunks(uris, 100))
        print 'chunks: ' + str(len(chunk_list))





        if schedule:
            programs = find_program(rows, int_to_day(offset_day.weekday()), schedule)
        for key, value in programs.iteritems():
            sp.user_playlist_add_tracks(username, key, value)
        # for each subgroup of 100 tracks or less, add all tracks to playlist
        for i in list(chunk_list):
            results = sp.user_playlist_add_tracks(username, playlist_id, i)


else:
    print "Can't get token"
