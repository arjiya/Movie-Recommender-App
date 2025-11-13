# main.py
import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import preprocess
from display import fetch_poster
import os
import pickle

# --- Load preprocessed DataFrame ---
@st.cache_data(show_spinner=False)
def load_data():
    os.makedirs("Files", exist_ok=True)
    path = "Files/new_df.pkl"
    if os.path.exists(path):
        return pd.read_pickle(path)
    df = preprocess()
    df.to_pickle(path)
    return df

# --- Load similarity matrix ---
@st.cache_data(show_spinner=False)
def load_similarity():
    path = "Files/similarity_tags.pkl"
    with open(path, "rb") as f:
        return pickle.load(f)

# --- Recommendation function ---
def recommend(movie_name, df, similarity):
    if movie_name not in df['title'].values:
        st.error("❌ Movie not found in dataset!")
        return []
    index = df[df['title'] == movie_name].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended = []
    for i in distances[1:11]:  # top 10 similar movies
        movie = df.iloc[i[0]]
        recommended.append((movie['title'], movie['poster_path'], movie['movie_id']))
    return recommended

# --- Streamlit UI ---
def main():
    st.set_page_config(layout="wide", page_title="🎬 Movie Recommendation System")
    
    # Centered, smaller, styled title
    st.markdown("""
    <h2 style="text-align:center; color:#black; font-family:Arial; font-size:28px; margin-top:10px;">
    🎥 Movie Recommendation System
    </h2>
    
    """, unsafe_allow_html=True)


    # st.info("🔄 Loading movie data...")
    df = load_data()
    similarity = load_similarity()

    st.sidebar.header("🎞️ Choose a Movie")
    movie_list = df['title'].values
    selected_movie = st.sidebar.selectbox("Select a movie:", movie_list)

    st.subheader(f"🎬 Selected Movie: {selected_movie}")
    

    if st.button("🔍 Show Recommendations"):
        st.success("Top 10 Recommended Movies:")
        recommended = recommend(selected_movie, df, similarity)

        # --- CSS to align all posters & text ---
        st.markdown("""
        <style>
        .movie-title {
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 14px;
            margin-bottom: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Split recommendations into rows of 5
        for row_movies in [recommended[:5], recommended[5:]]:
            cols = st.columns(5)
            for i, (title, poster_path, movie_id) in enumerate(row_movies):
                with cols[i]:
                    st.markdown(f'<div class="movie-title">{title}</div>', unsafe_allow_html=True)
                    st.image(fetch_poster(title, poster_path, movie_id), use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)  # Add space between rows

if __name__ == "__main__":
    main()
