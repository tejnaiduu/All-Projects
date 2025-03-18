from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load dataset
data = pd.read_csv(r"C:\Users\Charan\Documents\18_03_2025\All-Projects\kill_first\kill_backend\Coursera.csv")
data.fillna("", inplace=True)

# Normalize text to avoid duplicates due to case differences and spaces
data['Course Name'] = data['Course Name'].str.strip().str.lower()

# Combine relevant features for recommendations
data['tags'] = data['Course Name'] + " " + data['Course Description'] + " " + data['Skills']

# Remove duplicate course names
data = data.drop_duplicates(subset=['Course Name'], keep='first')

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['tags'])

# Train KNN model
knn = NearestNeighbors(n_neighbors=10, metric='cosine')  # Increased neighbors for better filtering
knn.fit(tfidf_matrix)

# Recommendation function using KNN
def recommend_course(course_name):
    course_name = course_name.strip().lower()  # Normalize input
    
    # Filter dataset based on Course Name
    filtered_data = data[data['Course Name'].str.contains(course_name, case=False, na=False)]
    
    if filtered_data.empty:
        return []
    
    # Take the index of the first matching course
    idx = filtered_data.index[0]
    
    # Perform KNN to recommend similar courses
    distances, indices = knn.kneighbors(tfidf_matrix[idx])
    
    # Sort and filter unique recommendations
    sorted_courses = sorted(zip(distances[0][1:], indices[0][1:]), key=lambda x: x[0])
    unique_courses = []
    seen = set()
    
    for _, idx in sorted_courses:
        course = data['Course Name'].iloc[idx]
        if course not in seen:
            unique_courses.append(course)
            seen.add(course)
    
    return unique_courses

# API endpoint
@app.route('/recommend', methods=['GET'])
def recommend():
    course_name = request.args.get('course_name')
    
    if not course_name:
        return jsonify({"error": "Course name is required"}), 400

    # Get recommended courses
    recommended_courses = recommend_course(course_name)
    
    return jsonify({"recommended_courses": recommended_courses})

if __name__ == '__main__':
    app.run(debug=True)
