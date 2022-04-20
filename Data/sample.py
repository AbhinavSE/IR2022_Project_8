from PIL import Image
import stagger
import io
import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
from pathlib import Path

imgFile = 'cover'
counter = 0
data = []

for file in Path('songs').glob('*'):
	fileName = str(file).split('\\')[-1]
	mp3 = stagger.read_tag('songs/' + fileName)
	print(counter, file)
	if stagger.id3.APIC in mp3:
		data.append([mp3.artist, mp3.album, mp3.title, mp3.genre, mp3.comment, f'/songs/{fileName}', f'/image/{imgFile}-{counter}.jpg'])
		by_data = mp3[stagger.id3.APIC][0].data
		im = io.BytesIO(by_data)
		imageFile = Image.open(im)
		imageFile.save(f'{imgFile}-{counter}.jpg')
	else:
		data.append([mp3.artist, mp3.album, mp3.title, mp3.genre, mp3.comment, f'/songs/{fileName}', ''])
	counter += 1

df = pd.DataFrame(data, columns = ['Artist', 'Album', 'Title', 'Genre', 'Comments', 'music_folder', 'image_folder'])
df.to_csv('metadata.csv', index = False)