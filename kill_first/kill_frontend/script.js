document.getElementById("recommendation-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent the form from refreshing the page

    // Get values from the input fields
    const courseName = document.getElementById("course_name").value;
    const difficultyLevel = document.getElementById("difficulty_level").value;

    // Validate inputs
    if (!courseName || !difficultyLevel) {
        showError("Please fill in both fields.");
        return;
    }

    // Clear any previous errors or recommendations
    document.getElementById("error-message").textContent = "";
    document.getElementById("recommended-courses").innerHTML = "";

    // Send request to Flask API
    fetch(`http://localhost:5000/recommend?course_name=${courseName}&difficulty_level=${difficultyLevel}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                showRecommendedCourses(data.recommended_courses);
            }
        })
        .catch(err => {
            showError("An error occurred while fetching recommendations.");
            console.error(err);
        });
});

// Function to display error messages
function showError(message) {
    document.getElementById("error-message").textContent = message;
}

// Function to display recommended courses
function showRecommendedCourses(courses) {
    const coursesList = document.getElementById("recommended-courses");

    if (courses.length === 0) {
        coursesList.innerHTML = "<li>No recommendations found.</li>";
        return;
    }

    courses.forEach(course => {
        const li = document.createElement("li");
        li.textContent = course;
        coursesList.appendChild(li);
    });
}
