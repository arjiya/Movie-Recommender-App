# compute_similarity.py
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

os.makedirs("Files", exist_ok=True)

# Load preprocessed movies dataframe
df = pd.read_pickle("Files/new_df.pkl")

# Create CountVectorizer and compute similarity
cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(df['tags']).toarray()
similarity = cosine_similarity(vectors)

# Save similarity matrix
with open("Files/similarity_tags.pkl", "wb") as f:
    pickle.dump(similarity, f)

print("✅ Similarity matrix saved.")
