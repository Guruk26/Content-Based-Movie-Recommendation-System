[1mdiff --git a/app.py b/app.py[m
[1mindex 4a335fa..90b9aca 100644[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@ -56,9 +56,9 @@[m [mdef build_model(df):[m
 # ============================================================[m
 # Step 4: Recommendation Function[m
 # ============================================================[m
[31m-def recommend(movie_name, df, cosine_sim, movie_indices, top_n=5):[m
[32m+[m[32mdef recommend(movie_name, df, cosine_sim, movie_indices, top_n=5, selected_genres=None):[m
     """[m
[31m-    Return top N movies similar to the given movie.[m
[32m+[m[32m    Return top N movies similar to the given movie, optionally filtered by genre.[m
     """[m
     # Find index of the selected movie[m
     idx = movie_indices[movie_name][m
[36m@@ -69,8 +69,20 @@[m [mdef recommend(movie_name, df, cosine_sim, movie_indices, top_n=5):[m
     # Sort by similarity score (highest first)[m
     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[m
 [m
[31m-    # Exclude the movie itself (index 0) and take top N[m
[31m-    sim_scores = sim_scores[1:top_n + 1][m
[32m+[m[32m    # Exclude the movie itself[m
[32m+[m[32m    sim_scores = sim_scores[1:][m
[32m+[m
[32m+[m[32m    # Keep movies matching at least one selected genre. Genres in the dataset[m
[32m+[m[32m    # are space-separated (for example, "Action Sci-Fi Thriller").[m
[32m+[m[32m    if selected_genres:[m
[32m+[m[32m        selected_genres = set(selected_genres)[m
[32m+[m[32m        sim_scores = [[m
[32m+[m[32m            score for score in sim_scores[m
[32m+[m[32m            if selected_genres.intersection(str(df['genre'].iloc[score[0]]).split())[m
[32m+[m[32m        ][m
[32m+[m
[32m+[m[32m    # Apply the existing recommendation-count selection after filtering.[m
[32m+[m[32m    sim_scores = sim_scores[:top_n][m
 [m
     # Get movie indices and scores[m
     movie_idx_list = [i[0] for i in sim_scores][m
[36m@@ -78,7 +90,7 @@[m [mdef recommend(movie_name, df, cosine_sim, movie_indices, top_n=5):[m
 [m
     # Build results DataFrame[m
     result = pd.DataFrame({[m
[31m-        'Rank': range(1, top_n + 1),[m
[32m+[m[32m        'Rank': range(1, len(movie_idx_list) + 1),[m
         'Movie Title': df['title'].iloc[movie_idx_list].values,[m
         'Genre': df['genre'].iloc[movie_idx_list].values,[m
         'Similarity Score': score_list[m
[36m@@ -126,6 +138,18 @@[m [mselected_movie = st.selectbox([m
 # Slider to choose number of recommendations[m
 top_n = st.slider('📋 Number of Recommendations:', min_value=1, max_value=10, value=5)[m
 [m
[32m+[m[32m# Genre filter options are derived from the dataset's space-separated genre values.[m
[32m+[m[32mavailable_genres = sorted({[m
[32m+[m[32m    genre[m
[32m+[m[32m    for genres in df['genre'].fillna('')[m
[32m+[m[32m    for genre in genres.split()[m
[32m+[m[32m})[m
[32m+[m[32mselected_genres = st.multiselect([m
[32m+[m[32m    '🎭 Filter Recommendations by Genre',[m
[32m+[m[32m    options=available_genres,[m
[32m+[m[32m    help='Select one or more genres to show recommendations matching any selected genre.'[m
[32m+[m[32m)[m
[32m+[m
 # Button to generate recommendations[m
 if st.button('🔍 Get Recommendations', type='primary'):[m
 [m
[36m@@ -136,18 +160,23 @@[m [mif st.button('🔍 Get Recommendations', type='primary'):[m
 [m
     # Generate recommendations[m
     st.markdown(f'### ✅ Top {top_n} Recommended Movies')[m
[31m-    recommendations = recommend(selected_movie, df, cosine_sim, movie_indices, top_n)[m
[31m-[m
[31m-    # Display as a table[m
[31m-    st.dataframe(recommendations, use_container_width=True, hide_index=True)[m
[31m-[m
[31m-    # Also show as individual cards[m
[31m-    st.markdown('### 📋 Recommendation Details')[m
[31m-    for _, row in recommendations.iterrows():[m
[31m-        with st.expander(f"#{int(row['Rank'])} {row['Movie Title']} (Score: {row['Similarity Score']})"):[m
[31m-            movie_detail = df[df['title'] == row['Movie Title']].iloc[0][m
[31m-            st.write(f"**Genre:** {movie_detail['genre']}")[m
[31m-            st.write(f"**Description:** {movie_detail['description']}")[m
[32m+[m[32m    recommendations = recommend([m
[32m+[m[32m        selected_movie, df, cosine_sim, movie_indices, top_n, selected_genres[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    if recommendations.empty:[m
[32m+[m[32m        st.info('No recommended movies match the selected genre filter. Try different genres or clear the filter.')[m
[32m+[m[32m    else:[m
[32m+[m[32m        # Display as a table[m
[32m+[m[32m        st.dataframe(recommendations, use_container_width=True, hide_index=True)[m
[32m+[m
[32m+[m[32m        # Also show as individual cards[m
[32m+[m[32m        st.markdown('### 📋 Recommendation Details')[m
[32m+[m[32m        for _, row in recommendations.iterrows():[m
[32m+[m[32m            with st.expander(f"#{int(row['Rank'])} {row['Movie Title']} (Score: {row['Similarity Score']})"):[m
[32m+[m[32m                movie_detail = df[df['title'] == row['Movie Title']].iloc[0][m
[32m+[m[32m                st.write(f"**Genre:** {movie_detail['genre']}")[m
[32m+[m[32m                st.write(f"**Description:** {movie_detail['description']}")[m
 [m
 st.markdown('---')[m
 st.caption('Assignment 20 — Building & Deploying a Recommendation System')[m
