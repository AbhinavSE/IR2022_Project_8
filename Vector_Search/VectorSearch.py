import pandas as pd
import joblib
import math
import numpy as np
import pickle as pkl
from filter import filter
import warnings

warnings.filterwarnings("ignore")


class VectorSearch:
    def __init__(self) -> None:
        with open("pickle_files/tf_idf_corpus.pkl", "rb") as f:
            self.corpus_matrix = joblib.load(f)

        with open("pickle_files/data.pkl", "rb") as f:
            self.data = pkl.load(f)

        with open("pickle_files/vocab.pkl", "rb") as f:
            self.vocab = pkl.load(f)

        with open("pickle_files/idf.pkl", "rb") as f:
            self.idf = pkl.load(f)

    def cosine(self, x, y) -> float:
        return x @ y / ((np.sum(x**2) ** 0.5) * (np.sum(y**2) ** 0.5))

    def query(self, query: str, k=10) -> list:
        query_posting_list = {}
        cleaned_query = filter(query, False)

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

        cosine_sim = {}

        for i in range(len(self.corpus_matrix)):
            cosine_sim[i] = {}
            cosine_sim[i][0] = self.cosine(query_vector[0][0], self.corpus_matrix[i][0])

        tf_ranking = sorted(cosine_sim.items(), key=lambda x: x[1][0], reverse=True)[:k]

        query_result = []
        df_index = []
        for doc_id, cosine_rank in tf_ranking:
            query_result.append((self.data.loc[doc_id]["Title"], cosine_rank[0]))
            df_index.append(doc_id)

        return query_result, df_index
