# create_new_df.py
import os
import pandas as pd
from preprocess import preprocess

os.makedirs("Files", exist_ok=True)

df = preprocess()
df.to_pickle("Files/new_df.pkl")

print("✅ new_df.pkl created successfully!")
