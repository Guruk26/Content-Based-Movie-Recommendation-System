import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# Step 1: Load the Dataset
# ============================================================
# Cache the data loading so it doesn't reload every time user interacts
@st.cache_data
def load_data():
    # Load movies CSV with title, genre and description columns
    df = pd.read_csv('movies.csv')
    return df

# ============================================================
# Step 2: Preprocess Text
# ============================================================
def clean_text(text):
    """
    Clean raw text:
    1. Lowercase
    2. Remove special characters
    3. Remove extra spaces
    """
    text = text.lower()                              # Lowercase
    text = re.sub(r'[^a-z0-9 ]', '', text)         # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()        # Remove extra spaces
    return text

# ============================================================
# Step 3: Build TF-IDF and Similarity Matrix
# ============================================================
@st.cache_data
def build_model(df):
    # Handle missing values
    df['genre'] = df['genre'].fillna('')
    df['description'] = df['description'].fillna('')

    # Combine genre (repeated for weight) + description
    df['clean_text'] = (df['genre'] + ' ' + df['genre'] + ' ' + df['description']).apply(clean_text)

    # Build TF-IDF matrix
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['clean_text'])

    # Compute cosine similarity between all movies
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Map movie title to its index
    movie_indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    return cosine_sim, movie_indices

# ============================================================
# Step 4: Recommendation Function
# ============================================================
def recommend(movie_name, df, cosine_sim, movie_indices, top_n=5):
    """
    Return top N movies similar to the given movie.
    """
    # Find index of the selected movie
    idx = movie_indices[movie_name]

    # Get similarity scores with all movies
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort by similarity score (highest first)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Exclude the movie itself (index 0) and take top N
    sim_scores = sim_scores[1:top_n + 1]

    # Get movie indices and scores
    movie_idx_list = [i[0] for i in sim_scores]
    score_list = [round(i[1], 4) for i in sim_scores]

    # Build results DataFrame
    result = pd.DataFrame({
        'Rank': range(1, top_n + 1),
        'Movie Title': df['title'].iloc[movie_idx_list].values,
        'Genre': df['genre'].iloc[movie_idx_list].values,
        'Similarity Score': score_list
    })
    return result

# ============================================================
# Step 5: Streamlit UI
# ============================================================

# Page configuration
st.set_page_config(
    page_title='Movie Recommendation System',
    page_icon='🎬',
    layout='centered'
)

# App title and description
st.title('🎬 Movie Recommendation System')
st.write('Select a movie below to get similar movie recommendations based on genre and plot.')
st.markdown('---')

# Load data and build model
df = load_data()
cosine_sim, movie_indices = build_model(df.copy())

# Sidebar with info
st.sidebar.title('ℹ️ About')
st.sidebar.write('**Type:** Content-Based Filtering')
st.sidebar.write('**Method:** TF-IDF + Cosine Similarity')
st.sidebar.write(f'**Movies in dataset:** {len(df)}')
st.sidebar.markdown('---')
st.sidebar.write('**How it works:**')
st.sidebar.write('1. Select a movie you like')
st.sidebar.write('2. Click Recommend')
st.sidebar.write('3. Get similar movies!')

# Dropdown to select a movie
selected_movie = st.selectbox(
    '🎥 Choose a Movie:',
    options=sorted(df['title'].tolist()),  # Sorted alphabetically for easy selection
    index=0
)

# Slider to choose number of recommendations
top_n = st.slider('📋 Number of Recommendations:', min_value=1, max_value=10, value=5)

# Button to generate recommendations
if st.button('🔍 Get Recommendations', type='primary'):

    # Show selected movie details
    movie_info = df[df['title'] == selected_movie].iloc[0]
    st.markdown('### 🎬 Selected Movie')
    st.info(f"**Title:** {movie_info['title']}  \n**Genre:** {movie_info['genre']}  \n**Description:** {movie_info['description']}")

    # Generate recommendations
    st.markdown(f'### ✅ Top {top_n} Recommended Movies')
    recommendations = recommend(selected_movie, df, cosine_sim, movie_indices, top_n)

    # Display as a table
    st.dataframe(recommendations, use_container_width=True, hide_index=True)

    # Also show as individual cards
    st.markdown('### 📋 Recommendation Details')
    for _, row in recommendations.iterrows():
        with st.expander(f"#{int(row['Rank'])} {row['Movie Title']} (Score: {row['Similarity Score']})"):
            movie_detail = df[df['title'] == row['Movie Title']].iloc[0]
            st.write(f"**Genre:** {movie_detail['genre']}")
            st.write(f"**Description:** {movie_detail['description']}")

st.markdown('---')
st.caption('Assignment 20 — Building & Deploying a Recommendation System')
