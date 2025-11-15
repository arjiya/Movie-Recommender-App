# movie_detail.py
import streamlit as st
import requests

API_KEY = "YOUR_TMDB_API_KEY"
BASE_URL = "https://api.themoviedb.org/3"

def show_movie_detail(movie_id):
    # Fetch movie details from TMDb
    res = requests.get(f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US")
    if res.status_code != 200:
        st.error("Movie not found")
        return

    movie_data = res.json()

    # Back button
    if st.button("⬅ Back"):
        st.session_state.selected_movie = None

    st.title(movie_data.get("title", "No Title"))
    poster = movie_data.get("poster_path")
    if poster:
        st.image(f"https://image.tmdb.org/t/p/w300{poster}")

    st.write("**Overview:**", movie_data.get("overview", "No overview available"))
    st.write("**Release Date:**", movie_data.get("release_date", "Unknown"))
    st.write("**Rating:**", movie_data.get("vote_average", "N/A"))
