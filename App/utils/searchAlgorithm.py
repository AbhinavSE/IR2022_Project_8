import pandas as pd
import time
import re
from collections import defaultdict
from pprint import pprint
import json
import lyricsgenius as lg
from PIL import Image
import stagger
import io
import numpy as np
import matplotlib.pyplot as plt


class Search:

    METADATA_LOC = 'assets/data/metadata.csv'

    def __init__(self):
        self.grams = {
            'uni': defaultdict(list),
            'bi': defaultdict(list),
            'tri': defaultdict(list)
        }
        self.map = defaultdict(list)
        self.initGrams()
        self.genius = lg.Genius('M18NYItwSvk9kctzrPF1rOlO7YAvFHUpSrepez3VT0FE81uKb8s5-BBkb-HhGHgg', skip_non_songs=True, remove_section_headers=True, excluded_terms=['(Remix)', '(Live)'])

    def addGrams(self, wordSet):
        for key in wordSet:
            for word in key.split():
                if word:
                    self.grams['uni'][word[0]].append(key)
                    if len(word) > 1:
                        self.grams['bi'][word[:2]].append(key)
                    if len(word) > 2:
                        self.grams['tri'][word[:3]].append(key)

    def getValues(self, value, splitWord=False):
        valueSet = set()

        for index, v in enumerate(value):
            v = v.lower()
            key = re.sub(r'[^\w\s]', ' ', v)
            if splitWord:
                for word in key.split():
                    self.map[word].append(index)
                    valueSet.add(word)
            else:
                self.map[key].append(index)
                valueSet.add(key)

        return valueSet

    def initGrams(self):
        dataset = pd.read_csv(self.METADATA_LOC)

        titles = self.getValues(dataset['Title'].values.tolist())
        albums = self.getValues(dataset['Album'].values.tolist())
        artist = self.getValues(dataset['Artist'].values.tolist(), splitWord=True)

        self.metadata = {
            'Title': titles,
            'Artist': artist,
            'Album': albums
        }

        self.addGrams(titles)
        self.addGrams(artist)
        self.addGrams(albums)

    def searchType(self, searchWord):
        r = re.compile('.*' + searchWord)

        if len(searchWord) == 1:
            result = self.grams['uni'].get(searchWord, [])
        elif len(searchWord) == 2:
            result = self.grams['bi'].get(searchWord, [])
        elif len(searchWord) == 3:
            result = self.grams['tri'].get(searchWord, [])
        else:
            result = list(filter(r.match, self.grams['tri'].get(searchWord[:3], [])))

        return result

    def searchSong(self, searchString):
        searchString = searchString.lower()

        result = self.searchType(searchString)

        if not result:
            for words in searchString.split():
                result += self.searchType(words)

        finalResult = []
        for r in result:
            for k in self.metadata:
                if r in self.metadata[k]:
                    finalResult.append([r, k])
                    break

        return finalResult

    def addSongToDB(self, data, lyricSearch):
        # data = (Artist, Title, Folder location)
        title = data[1]
        artistName = data[0]

        titles = self.getValues(title)  # Pass in title name
        self.metadata['Title'] = self.metadata['Title'].union(titles)
        self.addGrams(titles)

        artist = self.getValues(artistName)  # Pass in artist name
        self.metadata['Artist'] = self.metadata['Artist'].union(titles)
        self.addGrams(artist)

        # Initialize song meta data with Artist, Album, Title, Genre, Comments, Music folder, Image Folder
        songMetaData = {'Artist': artistName, 'Album': 'None', 'Title': title, 'Genre': 'None', 'Comments': 'None', 'music_folder': data[2]}

        # Getting cover image from the song file
        mp3 = stagger.read_tag(f'assets/data{data[2]}')
        if stagger.id3.APIC in mp3:
            by_data = mp3[stagger.id3.APIC][0].data
            im = io.BytesIO(by_data)
            imageFile = Image.open(im)
            imageFile.save(f'assets/data/image/{title}-cover.jpg')
            songMetaData['image_folder'] = f'assets/data/image/{title}-cover.jpg'  # Add image location

        # Adding it to metadata.csv
        data = pd.read_csv(self.METADATA_LOC)
        songMetaData['Id'] = len(data)
        data = data.append(songMetaData, ignore_index=True)
        data.to_csv(self.METADATA_LOC, index=False)

        # Getting the lyrics of the songs using genius library and adding it to index
        try:
            song = self.genius.search_song(title, artistName)
            lyricSearch.add_song_indexing(song.lyrics)
        except Exception as e:
            print('Lyrics not found')


if __name__ == '__main__':
    print('Started')
    s = Search()
    print('Loaded')

    with open('map.json', 'w') as outfile:
        json.dump(s.map, outfile)

    startTime = time.time()
    print(s.searchSong('ed '))
    print(time.time() - startTime)
