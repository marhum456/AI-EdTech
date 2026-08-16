// =====================================================
// API CONFIGURATION
// =====================================================

const API_BASE_URL = "http://127.0.0.1:8000";


// =====================================================
// COURSE DATA
// =====================================================

const courses = [

    // =====================================================
    // PHYSICS
    // =====================================================

    {
        subject: "physics",
        name: "Physics",
        description: "Learn Physics concepts and problem solving.",
        icon: "⚛️",

        lessons: [
            {
                course: "motion",
                lesson: "lesson_1",
                name: "Lesson 1 - Motion",
                pdf: `${API_BASE_URL}/uploads/physics/Physics-%20Motion.pdf`
            },

            {
                course: "work",
                lesson: "lesson_2",
                name: "Lesson 2 - Work",
                pdf: `${API_BASE_URL}/uploads/physics/Physics-%20Work.pdf`
            }
        ]
    },


    {
        subject: "mathematics",
        name: "Mathematics",
        description: "Learn mathematics concepts step by step.",
        icon: "📐",

        lessons: [
            {
                course: "Sets",
                lesson: "lesson_1",
                name: "Lesson 1 - Sets",
                pdf: "http://127.0.0.1:8000/uploads/Mathematics/Mathematics-%20Sets.pdf"
            },

            {
                course: "Geometry",
                lesson: "lesson_2",
                name: "Lesson 2 - Geometry",
                pdf: "http://127.0.0.1:8000/uploads/Mathematics/Mathematics-%20Geometry.pdf"
            },

            {
                course: "algebra",
                lesson: "lesson_3",
                name: "Lesson 3 - Algebra",
                pdf: "http://127.0.0.1:8000/uploads/Mathematics/Mathematics-%20Algebra.pdf"
            }
        ]
    },


    // =====================================================
    // WEB DEVELOPMENT
    // =====================================================

    {
        subject: "web_developement",
        name: "Web Development",
        description: "Learn HTML, CSS and JavaScript.",
        icon: "💻",

        lessons: [
            {
                course: "html",
                lesson: "lesson_1",
                name: "Lesson 1 - HTML",
                pdf: `${API_BASE_URL}/uploads/web_developement/HTML%20Fundamentals.pdf`
            },

            {
                course: "css",
                lesson: "lesson_2",
                name: "Lesson 2 - CSS",
                pdf: `${API_BASE_URL}/uploads/web_developement/CSS%20Fundamentals.pdf`
            },

            {
                course: "javascript",
                lesson: "lesson_3",
                name: "Lesson 3 - JavaScript",
                pdf: `${API_BASE_URL}/uploads/web_developement/JavaScript%20Fundamentals.pdf`
            }
        ]
    }
];

// =====================================================
// CURRENT STATE
// =====================================================

let currentCourse = null;
let currentLesson = null;

let currentQuiz = null;
let currentQuizId = null;
let currentModel = null;


// =====================================================
// SCREEN MANAGEMENT
// =====================================================

function hideAllScreens() {

    document
        .querySelectorAll(".screen")
        .forEach(screen => {
            screen.classList.add("hidden");
        });
}


// =====================================================
// SHOW COURSES
// =====================================================

function showCourses() {

    hideAllScreens();

    document
        .getElementById("courses-screen")
        .classList.remove("hidden");

    loadCourses();
}


// =====================================================
// LOAD COURSES
// =====================================================

function loadCourses() {

    const container =
        document.getElementById("courses-container");

    container.innerHTML = "";

    courses.forEach((course, index) => {

        const card =
            document.createElement("div");

        card.className = "course-card";

        card.innerHTML = `
            <div class="course-icon">
                ${course.icon}
            </div>

            <h2>
                ${course.name}
            </h2>

            <p>
                ${course.description}
            </p>

            <button
                class="primary-btn"
                onclick="openCourse(${index})"
            >
                Open Course
            </button>
        `;

        container.appendChild(card);
    });
}


// =====================================================
// OPEN COURSE
// =====================================================

function openCourse(index) {

    currentCourse = courses[index];

    console.log("Current course:", currentCourse);

    hideAllScreens();

    document
        .getElementById("lessons-screen")
        .classList.remove("hidden");

    document
        .getElementById("lessons-title")
        .textContent =
            currentCourse.name;

    loadLessons();
}


// =====================================================
// LOAD LESSONS
// =====================================================

function loadLessons() {

    const container =
        document.getElementById("lessons-container");

    container.innerHTML = "";

    currentCourse.lessons.forEach(
        (lesson, index) => {

            const card =
                document.createElement("div");

            card.className = "lesson-card";

            card.innerHTML = `
                <h3>
                    ${lesson.name}
                </h3>

                <p>
                    ${currentCourse.name}
                </p>

                <button
                    class="primary-btn"
                    onclick="openLesson(${index})"
                >
                    Open Lesson
                </button>
            `;

            container.appendChild(card);
        }
    );
}


// =====================================================
// OPEN LESSON / PDF
// =====================================================

function openLesson(index) {

    currentLesson =
        currentCourse.lessons[index];

    console.log("================================");
    console.log("Opening lesson");
    console.log("Subject:", currentCourse.subject);
    console.log("Course:", currentLesson.course);
    console.log("Lesson:", currentLesson.lesson);
    console.log("PDF:", currentLesson.pdf);
    console.log("================================");

    hideAllScreens();

    document
        .getElementById("pdf-screen")
        .classList.remove("hidden");

    document
        .getElementById("pdf-title")
        .textContent =
            currentLesson.name;

    document
        .getElementById("pdf-viewer")
        .src =
            currentLesson.pdf;
}


// =====================================================
// BACK TO LESSONS
// =====================================================

function showLessons() {

    hideAllScreens();

    document
        .getElementById("lessons-screen")
        .classList.remove("hidden");
}


// =====================================================
// COMPLETED READING
// =====================================================

function completeReading() {

    hideAllScreens();

    document
        .getElementById("quiz-info-screen")
        .classList.remove("hidden");

    document
        .getElementById("info-subject")
        .textContent =
            currentCourse.name;

    document
        .getElementById("info-course")
        .textContent =
            currentLesson.course;

    document
        .getElementById("info-lesson")
        .textContent =
            currentLesson.name;
}


// =====================================================
// SHOW QUIZ INFORMATION
// =====================================================

function showQuizInfo() {

    hideAllScreens();

    document
        .getElementById("quiz-info-screen")
        .classList.remove("hidden");
}


// =====================================================
// START QUIZ
// =====================================================

async function startQuiz() {

    const infoButton =
        document.querySelector(
            "#quiz-info-screen .primary-btn"
        );

    infoButton.disabled = true;
    infoButton.textContent = "Generating Quiz...";

    try {

        const requestData = {

            subject:
                currentCourse.subject,

            course:
                currentLesson.course,

            lesson:
                currentLesson.lesson,

            number_of_questions: 5
        };

        console.log("Generating quiz:");
        console.log(requestData);

        const response =
            await fetch(
                `${API_BASE_URL}/quiz/generate`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(requestData)
                }
            );

        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(error);
        }

        const data =
            await response.json();

        console.log("Quiz generated:", data);

        currentQuiz =
            data.quiz;

        currentQuizId =
            data.quiz_id;

        currentModel =
            data.route;

        console.log("Quiz ID:", currentQuizId);
        console.log("Model:", currentModel);

        displayQuiz();

    } catch (error) {

        console.error(
            "Quiz generation error:",
            error
        );

        alert(
            "Failed to generate quiz.\n\n" +
            error.message
        );

    } finally {

        infoButton.disabled = false;
        infoButton.textContent = "Start Quiz";
    }
}


// =====================================================
// DISPLAY QUIZ
// =====================================================

function displayQuiz() {

    hideAllScreens();

    document
        .getElementById("quiz-screen")
        .classList.remove("hidden");

    document
        .getElementById("quiz-title")
        .textContent =
            `${currentCourse.name} Quiz`;

    const container =
        document.getElementById(
            "quiz-container"
        );

    container.innerHTML = "";

    currentQuiz.forEach(
        (question, index) => {

            const card =
                document.createElement("div");

            card.className =
                "question-card";

            let optionsHTML = "";

            question.options.forEach(
                (option) => {

                    optionsHTML += `
                        <label class="option">

                            <input
                                type="radio"
                                name="question-${index}"
                                value="${escapeHTML(option)}"
                            >

                            ${escapeHTML(option)}

                        </label>
                    `;
                }
            );

            card.innerHTML = `

                <div class="question-number">
                    Question ${index + 1}
                </div>

                <div class="question-text">
                    ${escapeHTML(question.question)}
                </div>

                ${optionsHTML}
            `;

            container.appendChild(card);
        }
    );
}


// =====================================================
// SUBMIT QUIZ
// =====================================================

async function submitQuiz() {

    const answers = [];

    let unanswered = false;

    currentQuiz.forEach(
        (question, index) => {

            const selected =
                document.querySelector(
                    `input[name="question-${index}"]:checked`
                );

            if (!selected) {

                unanswered = true;
                return;
            }

            answers.push({

                question:
                    index + 1,

                selected_answer:
                    selected.value
            });
        }
    );


    if (unanswered) {

        document
            .getElementById("quiz-error")
            .textContent =
                "Please answer all questions before submitting.";

        return;
    }


    document
        .getElementById("quiz-error")
        .textContent = "";


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/quiz/submit`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            quiz_id:
                                currentQuizId,

                            answers:
                                answers
                        })
                }
            );


        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(error);
        }


        const result =
            await response.json();

        console.log(
            "Quiz submission:",
            result
        );

        showResult(result);


    } catch (error) {

        console.error(error);

        alert(
            "Failed to submit quiz.\n\n" +
            error.message
        );
    }
}


// =====================================================
// SHOW RESULT
// =====================================================

function showResult(result) {

    hideAllScreens();

    document
        .getElementById("result-screen")
        .classList.remove("hidden");


    document
        .getElementById("result-score")
        .textContent =
            `${result.score} / ${result.total_questions}`;


    document
        .getElementById("result-percentage")
        .textContent =
            `${result.percentage}%`;


    document
        .getElementById("result-model")
        .textContent =
            currentModel;


    document
        .getElementById("result-quiz-id")
        .textContent =
            currentQuizId;


    document
        .getElementById("result-progress-id")
        .textContent =
            result.progress_id;
}


// =====================================================
// HTML ESCAPE
// =====================================================

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}


// =====================================================
// INITIAL PAGE
// =====================================================

showCourses();