import lyricsgenius as lg
import pandas as pd
import re

genius = lg.Genius('M18NYItwSvk9kctzrPF1rOlO7YAvFHUpSrepez3VT0FE81uKb8s5-BBkb-HhGHgg', skip_non_songs = True, remove_section_headers = True, excluded_terms = ['(Remix)', '(Live)'])

dataframe = pd.read_csv('metadata.csv')
lyricsArr = []
songsProblems = []

for row in dataframe.iterrows():
	title = row[1].Title
	artist = re.split('[;,]', row[1].Artist)[0]
	# print(title, artist)
	try:
		song = genius.search_song(title, artist)
		lyricsArr.append(song.lyrics)
	except Exception as e:
		print(e)
		print(title, artist)
		lyricsArr.append('')
		songsProblems.append(title)

print('-'*50)

dataframe['lyrics'] = lyricsArr
dataframe.to_csv('metadata_temp.csv', index = False)

print(songsProblems)



