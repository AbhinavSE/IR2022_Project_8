
import pandas as pd
import joblib
import math
import numpy as np
import pickle as pkl
from utils.filter import filter, vocab as fil_vocab
import warnings

warnings.filterwarnings("ignore")


class VectorSearch:
    BASE = "utils"

    def __init__(self) -> None:
        with open(f"{self.BASE}/pickle_files/tf_idf_corpus.pkl", "rb") as f:
            self.corpus_matrix = joblib.load(f)

        with open(f"{self.BASE}/pickle_files/data.pkl", "rb") as f:
            self.data = pkl.load(f)

        with open(f"{self.BASE}/pickle_files/vocab.pkl", "rb") as f:
            self.vocab = pkl.load(f)

        with open(f"{self.BASE}/pickle_files/idf.pkl", "rb") as f:
            self.idf = pkl.load(f)

    def cosine(self, x, y) -> float:
        return x @ y / ((np.sum(x**2) ** 0.5) * (np.sum(y**2) ** 0.5))

    def create_vector(self, string: str, boolean: bool):
        query_posting_list = {}

        cleaned_query = filter(string, boolean)

        query_doc = {"Title": "query"}
        query_doc["filter_lyrics"] = cleaned_query

        for value in cleaned_query:
            query_posting_list[value] = {"query": cleaned_query[value]}

        query_vector = np.zeros((1, 1, len(self.vocab)))

        for j, word in enumerate(self.vocab):
            tf1 = 0
            tf3 = 0

            if word in query_posting_list:
                tf1 = query_posting_list[word]["query"]
                tf3 = math.log(1 + tf1)

            query_vector[0][0][j] = tf3 * self.idf[word]

        return query_vector

    def undo_addtion(self) -> str:
        with open(f"{self.BASE}/pickle_files/prev_tf_idf_corpus.pkl", "rb") as f:
            self.corpus_matrix = joblib.load(f)

        with open(f"{self.BASE}/pickle_files/prev_data.pkl", "rb") as f:
            self.data = pkl.load(f)

        with open(f"{self.BASE}/pickle_files/prev_vocab.pkl", "rb") as f:
            self.vocab = pkl.load(f)

        with open(f"{self.BASE}/pickle_files/prev_idf.pkl", "rb") as f:
            self.idf = pkl.load(f)

        pkl.dump(self.idf, open(f"{self.BASE}/pickle_files/idf.pkl", "wb"))
        joblib.dump(
            self.corpus_matrix,
            open(f"{self.BASE}/pickle_files/tf_idf_corpus.pkl", "wb"),
            compress=5,
        )
        pkl.dump(self.vocab, open(f"{self.BASE}/pickle_files/vocab.pkl", "wb"))
        pkl.dump(self.data, open(f"{self.BASE}/pickle_files/data.pkl", "wb"))

        return "undo successful"

    def posting_list(self):
        nested_posting_list = {}

        for index, files in self.data.iterrows():
            if not (
                type(files["filter_lyrics"]) == float
                and pd.isna(files["filter_lyrics"])
            ):
                for words in files["filter_lyrics"]:
                    if words in nested_posting_list:
                        if files["Title"] in nested_posting_list[words]:
                            nested_posting_list[words][files["Title"]] += 1
                        else:
                            nested_posting_list[words][files["Title"]] = 1
                    else:
                        nested_posting_list[words] = {}
                        nested_posting_list[words][files["Title"]] = 1

        idf = {}
        total_documents = len(self.data)

        for word in nested_posting_list:
            idf[word] = math.log(total_documents / len(nested_posting_list[word]) + 1)

        self.idf = idf
        pkl.dump(self.idf, open(f"{self.BASE}/pickle_files/idf.pkl", "wb"))

        corpus_matrix = np.zeros((total_documents, 1, len(self.vocab)))

        for i, doc in self.data.iterrows():
            for j, word in enumerate(list(self.vocab)):
                tf1 = 0
                tf3 = 0

                if doc["Title"] in nested_posting_list[word]:
                    tf1 = nested_posting_list[word][doc["Title"]]
                    tf3 = math.log(1 + tf1)

                corpus_matrix[i][0][j] = tf3 * idf[word]

        self.corpus_matrix = corpus_matrix
        joblib.dump(
            self.corpus_matrix,
            open(f"{self.BASE}/pickle_files/tf_idf_corpus.pkl", "wb"),
            compress=5,
        )

    def add_song_indexing(self, lyrics: str, title: str) -> str:
        pkl.dump(self.vocab, open(f"{self.BASE}/pickle_files/prev_vocab.pkl", "wb"))
        joblib.dump(
            self.corpus_matrix,
            open(f"{self.BASE}/pickle_files/prev_tf_idf_corpus.pkl", "wb"),
            compress=5,
        )
        pkl.dump(self.idf, open(f"{self.BASE}/pickle_files/prev_idf.pkl", "wb"))
        pkl.dump(self.data, open(f"{self.BASE}/pickle_files/prev_data.pkl", "wb"))

        cleaned_query = filter(lyrics, True)

        self.vocab = list(set(self.vocab).union(fil_vocab))
        pkl.dump(self.vocab, open(f"{self.BASE}/pickle_files/vocab.pkl", "wb"))

        self.data.loc[len(self.data.index)] = [
            "Artist",
            "None",
            title,
            "None",
            lyrics,
            cleaned_query,
        ]
        pkl.dump(self.data, open(f"{self.BASE}/pickle_files/data.pkl", "wb"))

        try:
            self.posting_list()
        except:
            return "Failed to add to the corpus"
        return "Successfully added to the corpus"

    def query(self, query: str, k=10) -> list:

        query_vector = self.create_vector(query, False)
        cosine_sim = {}

        for i in range(len(self.corpus_matrix)):
            cosine_sim[i] = {}
            cosine_sim[i][0] = self.cosine(query_vector[0][0], self.corpus_matrix[i][0])

        tf_ranking = sorted(cosine_sim.items(), key=lambda x: x[1][0], reverse=True)[:k]
        df_index = []
        query_result = []

        for doc_id, cosine_rank in tf_ranking:
            query_result.append((self.data.loc[doc_id]["Title"], cosine_rank[0]))
            df_index.append(doc_id)

        return query_result, df_index
