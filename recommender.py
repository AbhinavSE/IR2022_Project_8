import joblib
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd

# embeddings = joblib.load("Data/embeddings.pkl")
# kd_tree = NearestNeighbors(n_neighbors=30, algorithm='kd_tree').fit(embeddings)
# joblib.dump(kd_tree, "Data/kd_tree.pkl")


class Recommender:
    def __init__(self):
        '''
        Initializes the recommender class
        '''
        self.kd_tree = joblib.load("Data/kd_tree.pkl")
        self.embeddings = joblib.load("Data/embeddings.pkl")
        self.metadata = pd.read_csv("Data/metadata.csv")

    def generate_user_vector(self, songs_liked):
        '''
        Generates a user vector with the songs liked by the user
        input:
            songs_liked: list of song IDs liked by the user

        output:
            user_vector: numpy array of the user's embedding
        '''
        user_vector = np.mean(self.embeddings[songs_liked], axis=0)
        return user_vector

    def get_recommendations(self, user_vector, k=10):
        '''
        Gets the k nearest neighbors of the user vector
        input:
            user_vector: numpy array of the user's embedding
            k: number of neighbors to return

        output:
            recommendations: list of song IDs of the k nearest neighbors
        '''
        distances, indices = self.kd_tree.kneighbors(user_vector.reshape(1, -1))
        recommendations = []
        for i in indices[0][:k]:
            recommendations.append(i)
        return recommendations


rec = Recommender()
print(rec.embeddings.shape)
songs_liked = [0, 1, 2]
print("generating user vector...")
user_vector = rec.generate_user_vector(songs_liked)
print("getting recommendations...")
recommendations = rec.get_recommendations(user_vector)
print(recommendations)
