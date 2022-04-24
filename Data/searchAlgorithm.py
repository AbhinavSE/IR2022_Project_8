from pytrie import StringTrie
import pandas as pd
import time
import re
from collections import defaultdict
from pprint import pprint
import json

class Search:

	def __init__(self):
		self.grams = {
			'uni': defaultdict(list),
			'bi': defaultdict(list),
			'tri': defaultdict(list)
		}
		self.map = defaultdict(list)
		self.initGrams()

		

	def addGrams(self, wordSet):
		for key in wordSet:
			for word in key.split():
				if word:
					self.grams['uni'][word[0]].append(key)
					if len(word) > 1:
						self.grams['bi'][word[:2]].append(key)
					if len(word) > 2:
						self.grams['tri'][word[:3]].append(key)
	
	def getValues(self, value, splitWord = False):
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
		dataset = pd.read_csv('metadata.csv')
		
		titles = self.getValues(dataset['Title'].values.tolist())
		albums = self.getValues(dataset['Album'].values.tolist())
		artist = self.getValues(dataset['Artist'].values.tolist(), splitWord = True)

		self.metadata = {
					'Title': titles,
					'Artist': artist,
					'Album': albums
					}

		self.addGrams(titles)
		self.addGrams(artist)
		self.addGrams(albums)

		pprint(self.grams)

	def searchSong(self, searchString):
		searchString = searchString.lower()
		r = re.compile('.*' + searchString)

		if len(searchString) == 1:
			result = self.grams['uni'].get(searchString, [])
		elif len(searchString) == 2:
			result = self.grams['bi'].get(searchString, [])
		elif len(searchString) == 3:
			result = self.grams['tri'].get(searchString, [])
		else:
			result = list(filter(r.match, self.grams['tri'].get(searchString[:3], [])))

		if not result:
			if len(searchString.split()) > 1:
				for words in searchString.split():
					result += list(filter(r.match, self.grams['tri'].get(searchString[:3], [])))
		

		finalResult = []
		for r in result:
			for k in self.metadata:
				if r in self.metadata[k]:
					finalResult.append([r, k])
					break

		return finalResult

if __name__ == '__main__':	
	print('Started')
	s = Search()
	print('Loaded')

	with open('map.json', 'w') as outfile:
		json.dump(s.map, outfile)

	startTime = time.time()
	print(s.searchSong('cha'))
	print(time.time() - startTime)






