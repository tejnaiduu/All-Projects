from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from flask_cors import CORS

app = Flask(__name__)  # Corrected here
CORS(app)

# Load dataset
data = pd.read_csv(r"C:\Users\Charan\Desktop\KILL PROJECT\killl\kill_backend\Coursera.csv")
data.fillna("", inplace=True)
data['tags'] = data['Course Name'] + " " + data['Difficulty Level'] + " " + data['Course Description'] + " " + data['Skills']

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['tags'])

# Train KNN model
knn = NearestNeighbors(n_neighbors=6, metric='cosine')
knn.fit(tfidf_matrix)

# Recommendation function using KNN
def recommend_course(course_name, difficulty_level):
    # Filter data based on Course Name and Difficulty Level
    filtered_data = data[(data['Course Name'].str.contains(course_name, case=False, na=False)) &
                          (data['Difficulty Level'].str.contains(difficulty_level, case=False, na=False))]
    
    if filtered_data.empty:
        return []
    
    # Take the index of the first matching course
    idx = filtered_data.index[0]
    
    # Perform KNN to recommend similar courses
    distances, indices = knn.kneighbors(tfidf_matrix[idx])
    
    # Return recommended course names (excluding the input course itself)
    return [data['Course Name'].iloc[i] for i in indices[0][1:]]

# API endpoint
@app.route('/recommend', methods=['GET'])
def recommend():
    course_name = request.args.get('course_name')
    difficulty_level = request.args.get('difficulty_level')
    
    if not course_name or not difficulty_level:
        return jsonify({"error": "Both course name and difficulty level are required"}), 400

    # Get recommended courses
    recommended_courses = recommend_course(course_name, difficulty_level)
    
    return jsonify({"recommended_courses": recommended_courses})

if __name__ == '__main__':  # Corrected here
    app.run(debug=True)
