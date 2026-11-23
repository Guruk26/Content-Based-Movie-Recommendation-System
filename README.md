# Assignment 20: Building & Deploying a Content-Based Movie Recommendation System

## 📌 Project Overview
This project fulfills **Assignment 20: Building & Deploying a Recommendation System**. It implements an end-to-end Machine Learning pipeline that:
1. Loads and preprocesses text data from a movie dataset.
2. Performs text vectorization using **TF-IDF (Term Frequency - Inverse Document Frequency)**.
3. Computes item similarity using **Cosine Similarity**.
4. Builds a recommendation logic function to retrieve the top $N$ most similar movies.
5. Deploys an interactive web interface using **Streamlit**.
6. Outlines full setup steps for **Git/GitHub** version control and **Render** cloud deployment.

---

## 📊 Dataset Details
- **Dataset Name:** Top Rated Movies Dataset (Adapted from Kaggle)
- **Source Reference:** [Kaggle TMDB Movie Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- **File:** `movies.csv`
- **Features Used:**
  - `title`: Unique item identifier (Movie Name)
  - `genre`: Categorical tags (Action, Sci-Fi, Drama, etc.)
  - `description`: Textual plot summary / overview
  - `clean_text`: Combined & cleaned text feature used for recommendation

---

## 📁 Repository Structure
```
Task20/
├── app.py                                   # Streamlit interactive web application
├── movies.csv                               # Movie dataset (Title, Genre, Description)
├── requirements.txt                         # Dependencies for local run & Render deployment
├── task20_recommendation_system.ipynb       # Jupyter Notebook solving all Part 1 - Part 6 tasks
├── README.md                                # Project documentation and deployment guide
└── GenAI - A20_ Building & Deploying a Recommendation System.pdf  # Assignment specifications
```

---

## 🧩 Tasks Covered & Workflow

### **Part 1 — Data Preprocessing**
- **Task 1: Load & Understand Dataset**: Loaded dataset using `pandas`, inspected `.shape`, column names, `.info()`, checked missing values (`.isnull().sum()`), and identified key text features.
- **Task 2: Text Preprocessing**: Handled missing values (`.fillna('')`), lowercased text, stripped punctuation and non-alphanumeric characters with regex, combined `genre` and `description` to emphasize both genre and storyline, and stored the result in `clean_text`.

### **Part 2 — Text Vectorization**
- **Task 3: TF-IDF Vectorization**: Used `TfidfVectorizer(max_features=5000, ngram_range=(1,2), stop_words='english')` to extract unigrams and bigrams while ignoring generic stopwords.
- **Task 4: Similarity Computation**: Computed pairwise **Cosine Similarity** matrix across all movies.  
  *Why Cosine Similarity?* Cosine similarity evaluates the cosine of the angle between two multi-dimensional vectors regardless of vector magnitude/text length, making it ideal for text comparison.

### **Part 3 — Recommendation Logic**
- **Task 5: Recommendation Function**:
  ```python
  def recommend(movie_name, top_n=5):
      # Finds index -> calculates pairwise scores -> sorts descending -> returns top N
  ```
  Verified recommendations across multiple genres (e.g., *The Dark Knight*, *Toy Story*, *Interstellar*).

### **Part 4 — Simple App Interface**
- **Task 6: Streamlit UI (`app.py`)**: Built an interactive UI featuring:
  - Dropdown menu to pick any movie from the dataset.
  - Slider to choose how many recommendations to display ($1$ to $10$).
  - Clean table output and expandable detail cards displaying genres and descriptions.

### **Part 5 — Version Control with Git & GitHub**
- **Task 7: Git Setup**: Step-by-step commands to push the project repository to GitHub.

### **Part 6 — Deployment on Render**
- **Task 8 & 9: Render Deployment**: Complete configuration for hosting on Render with live URL validation.

---

## ⚙️ Installation & Local Setup

### 1. Clone or Open the Project Directory
```bash
cd Task20
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

### 3. Run the Jupyter Notebook
To see all tasks executed step-by-step with markdown explanations:
```bash
jupyter notebook task20_recommendation_system.ipynb
```

### 4. Run the Streamlit Web Application
To launch the interactive app locally in your browser:
```bash
streamlit run app.py
```
The app will automatically open at `http://localhost:8501`.

---

## 🌐 Deployment Guide (Render)

Follow these steps to deploy on [Render](https://render.com):

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Assignment 20: Movie Recommendation System"
   git branch -M main
   git remote add origin https://github.com/<YOUR_USERNAME>/<REPO_NAME>.git
   git push -u origin main
   ```
2. **Create Web Service on Render**:
   - Log into [Render Dashboard](https://dashboard.render.com/).
   - Click **New +** → **Web Service**.
   - Connect your GitHub repository.
3. **Configure Service Settings**:
   - **Name:** `movie-recommender-system` (or your choice)
   - **Environment:** `Python 3`
   - **Region:** Any close to you (e.g., Singapore, Frankfurt, Oregon)
   - **Branch:** `main`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     streamlit run app.py --server.port $PORT --server.address 0.0.0.0
     ```
4. **Deploy**:
   - Click **Create Web Service**.
   - Render will build the environment and provide your live application link (e.g., `https://movie-recommender-system.onrender.com`).
5. **Validation**:
   - Open the live URL.
   - Choose a movie from the dropdown, click **Get Recommendations**, and verify the returned recommendations.

---

## 💡 Tech Stack
- **Language:** Python 3.9+
- **Data Manipulation:** `pandas`, `numpy`
- **Machine Learning:** `scikit-learn` (`TfidfVectorizer`, `cosine_similarity`)
- **Web App / UI:** `streamlit`
- **Cloud Hosting:** Render
