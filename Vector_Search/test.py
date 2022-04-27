from VectorSearch import VectorSearch

x = VectorSearch()
print(x.query("you to hit the pedal", 2))
print(x.query("shape of you", 5))
print(len(x.data))
print(x.add_song_indexing("I walk this empty street on the boulevard of broken dream."))
print(len(x.data))
print(x.query("you to hit the pedal", 2))
print(x.query("shape of you", 5))
print(x.query("empty street", 5))
print(x.query("boulevard of broken dream", 5))
print(x.undo_addtion())
