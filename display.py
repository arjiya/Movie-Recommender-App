import requests
import os
import pickle
import streamlit as st

# Folder & cache setup
CACHE_DIR = "Files"
POSTER_CACHE_FILE = os.path.join(CACHE_DIR, "poster_cache.pkl")
os.makedirs(CACHE_DIR, exist_ok=True)

# Load existing cache if available
if os.path.exists(POSTER_CACHE_FILE):
    with open(POSTER_CACHE_FILE, "rb") as f:
        poster_cache = pickle.load(f)
else:
    poster_cache = {}

# ------------------------------
# Function: Fetch poster URL
# ------------------------------
@st.cache_data(show_spinner=False)
def fetch_poster(title, poster_path=None, movie_id=None):
    """
    Returns poster URL. Priority:
    1. CSV poster_path
    2. Local cache
    3. TMDb API (by movie_id or title)
    4. Placeholder if not found
    Caches all fetched posters locally.
    """

    # 1️⃣ CSV poster exists
    if poster_path:
        poster_cache[title] = poster_path
        return poster_path

    # 2️⃣ Check local cache
    if title in poster_cache:
        return poster_cache[title]

    # 3️⃣ Fetch from TMDb API
    api_key = "82a762e6b888c3aa1c028b3dc93aa4b3"
    poster_url = None

    # Try by movie_id first
    if movie_id:
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
            data = requests.get(url, timeout=5).json()
            if 'poster_path' in data and data['poster_path']:
                poster_url = "https://image.tmdb.org/t/p/w500" + data['poster_path']
        except:
            pass

    # Fallback: search by title
    if not poster_url:
        try:
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
            search_data = requests.get(search_url, timeout=5).json()
            if search_data.get('results'):
                poster_path_api = search_data['results'][0].get('poster_path')
                if poster_path_api:
                    poster_url = "https://image.tmdb.org/t/p/w500" + poster_path_api
        except:
            pass

    # 4️⃣ Final fallback: placeholder
    if not poster_url:
        poster_url = "https://via.placeholder.com/500x750?text=No+Poster+Available"

    # Save to local cache
    poster_cache[title] = poster_url
    with open(POSTER_CACHE_FILE, "wb") as f:
        pickle.dump(poster_cache, f)

    return poster_url

# ------------------------------
# Function: Display movie details
# ------------------------------
def show_movie_details(movie):
    """
    Displays detailed information about a movie.
    """
    st.image(fetch_poster(movie['title'], movie.get('poster')), use_container_width=True)
    st.markdown(f"### 🎬 {movie['title']}")
    st.markdown(f"**🎞️ Director:** {movie.get('director', 'Unknown')}")
    st.markdown(f"**🧑‍🎤 Cast:** {', '.join(movie['cast']) if isinstance(movie.get('cast'), list) else movie.get('cast', 'N/A')}")
    st.markdown(f"**🎭 Genres:** {', '.join(movie['genres']) if isinstance(movie.get('genres'), list) else movie.get('genres', 'N/A')}")
    st.markdown(f"**📝 Overview:** {movie.get('overview', 'No overview available.')}")

