import re
import requests
import sys
import time
import urllib
from bs4 import BeautifulSoup

search_url = 'https://mojim.com/song_name.html?t3'
lrc_url = 'https://mojim.com/twthxsong_idx1.htm'

def get_song_id(song_name):
    req = requests.get(search_url.replace('song_name', song_name))
    data = req.text

    soup = BeautifulSoup(data, 'lxml')
    spans = soup.findAll('span', {
        'class': 'mxsh_ss4'
    })

    patt = re.compile(r"(.*?) " )

    for sp in spans:
        a = sp.find('a', {
            'title': patt
        })
        if a != None:
            return a.attrs['href'].replace('/twy', '').replace('.htm', '')
    return None

def get_song_lrc(song_id):
    req = requests.get(lrc_url.replace('song_id', song_id))
    data = req.text
    soup = BeautifulSoup(data, "html.parser")
    tags = soup.find_all("textarea")
    dec = str(tags[0]).split('\n',1)[1].replace("</textarea>","")
    dec = dec.split('\n')
    return dec

def start(song_name):
    song_id = get_song_id(song_name)
    if song_id is not None:
        print(song_id)
        lrc = get_song_lrc(song_id)
        print(lrc)
        f = open(".\\lrc\\{}.txt".format(song_name), 'w+', encoding='utf-8')
        for lrc_line in lrc:
            f.write("{}\n".format(lrc_line))
        f.close()
    else:
        print("No result")
if __name__ == '__main__':
    params = len(sys.argv)
    if params == 2:
        song_name = sys.argv[1]
        start(song_name)
    if params < 2:
        print('Error format')
        print('Ex. python .\get_lrc.py \"告白氣球\"')