import requests
import unicodedata
import json
import spotipy
sp = spotipy.Spotify()
import spotipy.util as util
from functions import *
from bs4 import BeautifulSoup as bs4
from row import Row

def get_ckua_tracks(url):
    # TODO: set date properly

    f = requests.get(url)
    soup = bs4(f.content,'html.parser')
    table = soup.find("div", { "class" : "song-list" })
    rows = []
    table = table.find_all("div", { "class" : "row" })
    for i,value in enumerate(table):
        #  if i < 2:
            values = value.find_all("div", {"class" : "col-xs-3"})
            try:
                rows.append(Row(values[0].contents[0].encode('utf-8'), values[1].contents[0].encode('utf-8'), values[2].contents[0].encode('utf-8'), values[3].contents[0].encode('utf-8')))
            except:
                print ' \n empty cells messed this up (probably) \n'
    return rows
