document.getElementById("recommendation-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent form refresh

    const courseName = document.getElementById("course_name").value.trim();

    if (!courseName) {
        showError("⚠ Please enter a course name.");
        return;
    }

    // Clear errors and previous recommendations
    document.getElementById("error-message").textContent = "";
    document.getElementById("recommended-courses").innerHTML = "";

    // Fetch recommendations from the Flask API
    fetch(`http://localhost:5000/recommend?course_name=${encodeURIComponent(courseName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                showRecommendedCourses(data.recommended_courses);
            }
        })
        .catch(err => {
            showError("❌ Error fetching recommendations.");
            console.error(err);
        });
});

// Show error message
function showError(message) {
    document.getElementById("error-message").textContent = message;
}

// Display recommended courses
function showRecommendedCourses(courses) {
    const coursesList = document.getElementById("recommended-courses");

    if (courses.length === 0) {
        coursesList.innerHTML = "<li>😞 No recommendations found.</li>";
        return;
    }

    courses.forEach(course => {
        const li = document.createElement("li");
        li.textContent = course;
        coursesList.appendChild(li);
    });
}
