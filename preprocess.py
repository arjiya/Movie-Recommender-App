import pandas as pd
import ast

def preprocess():
    movies = pd.read_csv("movies.csv")
    credits = pd.read_csv("credits.csv")
    posters = pd.read_csv("poster.csv")

    # Merge datasets
    df = movies.merge(credits, on='title', how='left')
    df = df.merge(posters, on='title', how='left')

    df.fillna('', inplace=True)

    # Convert JSON-like strings to lists
    def convert(obj):
        try:
            L = []
            for i in ast.literal_eval(obj):
                L.append(i['name'])
            return L
        except:
            return []

    df['genres'] = df['genres'].apply(convert)
    df['cast'] = df['cast'].apply(convert)
    df['crew'] = df['crew'].apply(convert)

    # Extract director from crew
    def get_director(crew_list):
        for i in crew_list:
            if isinstance(i, dict) and i.get('job') == 'Director':
                return i.get('name', '')
        return ''

    df['director'] = df['crew'].apply(get_director)

    # Create a 'tags' column for text similarity
    df['tags'] = (
        df['overview'].astype(str) + " " +
        df['genres'].astype(str) + " " +
        df['cast'].astype(str) + " " +
        df['director'].astype(str)
    )

    # Clean duplicates
    df.drop_duplicates(subset=['title'], inplace=True)

    # Select relevant columns
    new_df = df[['title', 'overview', 'director', 'cast', 'genres', 'poster', 'tags']]
    return new_df
