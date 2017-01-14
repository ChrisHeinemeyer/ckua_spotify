import requests
import re
import unicodedata
import json
import spotipy
sp = spotipy.Spotify()
import spotipy.util as util
from functions import *
from bs4 import BeautifulSoup as bs4
from row import Row
import datetime
import ckua_web as ckua
CLIENT_ID = 'beee62c8844a49b48128f4fbc83ba723'
CLIENT_SECRET = '3d3c446958b54431ba8c4dc9b4a8d8cc'
REDIRECT_URI = 'http://localhost:3000'
username = 'ckua'
playlist_id = '7wSU1Mf1AWj71ZESoce3Hp'

def trim_unknowns(arr):
    indices = []
    for index, item in enumerate(arr):
        if item.uri is 'NONE':
            # print 'index ' + str(index) + ' is not found'
            indices.append(index)
    indices.reverse()
    for item in indices:
        del arr[item]
    return arr

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def get_uris(rows):
    #print "\n\n\n"
    uris = []
    for j, val in enumerate(rows):
        print str(j) + ' of ' + str(len(rows)) + ' searched'
        obj = sp.search(q=str(rows[j]), type='track', limit=1)
        if obj["tracks"]["total"] > 0:
        	rows[j].set_uri(obj["tracks"]["items"][0]["uri"])
        else:
            print 'could not find ' + str(rows[j])

    rows = trim_unknowns(rows)
    print str(len(rows)) + ' found on spotify'

    for j,val in enumerate(rows):
        uris.append(rows[j].uri)

    return uris

def find_program(rows, day, schedule):
    #
    show_tracks = {}
    count = 0
    for item in rows:
        if item.uri != 'NONE':
            m = re.search('[0-9]+:', item.time)
            t  = re.search('[0-9]+', m.group(0))
            time =  int(t.group(0))
            if(item.time.find('PM') != -1 and time != 12):
                time += 12
            for program in schedule['shows']:
                for slot in program['times']:
                    if day == slot['day'] and time >= slot['start time'] and  time < slot['end time']:
                        if 'uri' in program:
                            if program['uri'] not in show_tracks:
                                show_tracks[program['uri']] = []
                            show_tracks[program['uri']].append(item.uri)
                            count += 1
            
    return show_tracks



def int_to_day(num):
    return {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6 : 'Sunday'
    }[num]
