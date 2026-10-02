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

        courses: [



            {
                course: "work",
                name: "Work",
                description: "Learn the fundamentals of work in physics.",

                lessons: [

                    {
                        lesson: "lesson_1",
                        name: "Lesson 1 - Work_Basics",
                        pdf: `${API_BASE_URL}/uploads/physics/Physics-%20Work.pdf`
                    }

                ]
            }

        ]
    },


    // =====================================================
    // MATHEMATICS
    // =====================================================

    {
        subject: "mathematics",
        name: "Mathematics",
        description: "Learn mathematics concepts step by step.",
        icon: "📐",

        courses: [

            {
                course: "sets",
                name: "Sets",
                description: "Learn the fundamentals of sets.",

                lessons: [

                    {
                        lesson: "lesson_1",
                        name: "Lesson 1 - Sets_Basics",
                        pdf: `${API_BASE_URL}/uploads/Mathematics/Mathematics-%20Sets.pdf`
                    }

                ]
            },

            {
                course: "geometry",
                name: "Geometry",
                description: "Learn geometry concepts.",

                lessons: [

                    {
                        lesson: "lesson_1",
                        name: "Lesson 1 - Geometry_Basics",
                        pdf: `${API_BASE_URL}/uploads/Mathematics/Mathematics-%20Geometry.pdf`
                    }

                ]
            }

        ]
    },


    // =====================================================
    // COMPUTER SCIENCE
    // =====================================================

    {
        subject: "computer_science",
        name: "Computer Science",
        description: "Learn programming and modern computing concepts.",
        icon: "💻",

        courses: [

            // =================================================
            // WEB DEVELOPMENT COURSE
            // =================================================

            {
                course: "web_development",
                name: "Web Development",
                description: "Learn HTML, CSS and JavaScript.",

                lessons: [

                    {
                        lesson: "lesson_1",
                        name: "Lesson 1 - HTML Fundamentals",
                        pdf: `${API_BASE_URL}/uploads/computer_science/HTML%20Fundamentals.pdf`
                    },

                    {
                        lesson: "lesson_2",
                        name: "Lesson 2 - CSS Fundamentals",
                        pdf: `${API_BASE_URL}/uploads/computer_science/CSS%20Fundamentals.pdf`
                    },

                    {
                        lesson: "lesson_3",
                        name: "Lesson 3 - JavaScript Fundamentals",
                        pdf: `${API_BASE_URL}/uploads/computer_science/JavaScript%20Fundamentals.pdf`
                    }

                ]
            }

        ]
    }

];


// =====================================================
// CURRENT STATE
// =====================================================

let currentSubject = null;
let currentCourse = null;
let currentLesson = null;

let currentQuiz = null;
let currentQuizId = null;
let currentModel = null;


// =====================================================
// DOM ELEMENTS
// =====================================================

const subjectsSection =
    document.getElementById("subjects-section");

const coursesSection =
    document.getElementById("courses-section");

const lessonsSection =
    document.getElementById("lessons-section");

const pdfSection =
    document.getElementById("pdf-section");

const quizSection =
    document.getElementById("quiz-section");

const resultSection =
    document.getElementById("result-section");


// =====================================================
// HIDE ALL SECTIONS
// =====================================================

function hideAllSections() {

    subjectsSection.classList.add("hidden");
    coursesSection.classList.add("hidden");
    lessonsSection.classList.add("hidden");
    pdfSection.classList.add("hidden");
    quizSection.classList.add("hidden");
    resultSection.classList.add("hidden");
}


// =====================================================
// SHOW SUBJECTS
// =====================================================

function showSubjects() {

    hideAllSections();

    subjectsSection.classList.remove("hidden");

    loadSubjects();
}


// =====================================================
// LOAD SUBJECTS
// =====================================================

function loadSubjects() {

    const container =
        document.getElementById("subjects-container");

    container.innerHTML = "";

    courses.forEach((subject, index) => {

        const card =
            document.createElement("div");

        card.className = "course-card";

        card.innerHTML = `

            <div class="course-icon">
                ${subject.icon}
            </div>

            <h2>
                ${subject.name}
            </h2>

            <p>
                ${subject.description}
            </p>

            <button
                class="primary-button"
                onclick="openSubject(${index})">

                Open Subject

            </button>
        `;

        container.appendChild(card);
    });
}


// =====================================================
// OPEN SUBJECT
// =====================================================

function openSubject(index) {

    currentSubject = courses[index];

    console.log("================================");
    console.log("Opening Subject");
    console.log("Subject:", currentSubject.subject);
    console.log("================================");

    hideAllSections();

    coursesSection.classList.remove("hidden");

    document
        .getElementById("selected-subject-name")
        .textContent =
            currentSubject.name;

    loadCourses();
}


// =====================================================
// LOAD COURSES
// =====================================================

function loadCourses() {

    const container =
        document.getElementById("courses-container");

    container.innerHTML = "";

    currentSubject.courses.forEach(
        (course, index) => {

            const card =
                document.createElement("div");

            card.className = "course-card";

            card.innerHTML = `

                <h2>
                    ${course.name}
                </h2>

                <p>
                    ${course.description}
                </p>

                <button
                    class="primary-button"
                    onclick="openCourse(${index})">

                    Open Course

                </button>
            `;

            container.appendChild(card);
        }
    );
}


// =====================================================
// OPEN COURSE
// =====================================================

function openCourse(index) {

    currentCourse =
        currentSubject.courses[index];

    console.log("================================");
    console.log("Opening Course");
    console.log("Subject:", currentSubject.subject);
    console.log("Course:", currentCourse.course);
    console.log("================================");

    hideAllSections();

    lessonsSection.classList.remove("hidden");

    document
        .getElementById("selected-course-name")
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



                <button
                    class="primary-button"
                    onclick="openLesson(${index})">

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
    console.log("Opening Lesson");
    console.log("Subject:", currentSubject.subject);
    console.log("Course:", currentCourse.course);
    console.log("Lesson:", currentLesson.lesson);
    console.log("PDF:", currentLesson.pdf);
    console.log("================================");

    hideAllSections();

    pdfSection.classList.remove("hidden");

    document
        .getElementById("selected-lesson-name")
        .textContent =
            currentLesson.name;

    document
        .getElementById("pdf-viewer")
        .src =
            currentLesson.pdf;

    // Reset checkbox
    const checkbox =
        document.getElementById(
            "read-pdf-checkbox"
        );

    checkbox.checked = false;

    // Disable quiz button
    document
        .getElementById("generate-quiz-button")
        .disabled = true;

    document
        .getElementById("quiz-status")
        .textContent = "";
}


// =====================================================
// PDF READ CHECKBOX
// =====================================================

document
    .getElementById("read-pdf-checkbox")
    .addEventListener(
        "change",
        function () {

            const quizButton =
                document.getElementById(
                    "generate-quiz-button"
                );

            quizButton.disabled =
                !this.checked;
        }
    );


// =====================================================
// GENERATE QUIZ BUTTON
// =====================================================

document
    .getElementById("generate-quiz-button")
    .addEventListener(
        "click",
        startQuiz
    );


// =====================================================
// BACK TO SUBJECTS
// =====================================================

document
    .getElementById("back-to-subjects")
    .addEventListener(
        "click",
        showSubjects
    );


// =====================================================
// BACK TO COURSES
// =====================================================

document
    .getElementById("back-to-courses")
    .addEventListener(
        "click",
        function () {

            hideAllSections();

            coursesSection.classList.remove(
                "hidden"
            );

            loadCourses();
        }
    );


// =====================================================
// BACK TO LESSONS
// =====================================================

document
    .getElementById("back-to-lessons")
    .addEventListener(
        "click",
        function () {

            hideAllSections();

            lessonsSection.classList.remove(
                "hidden"
            );

            loadLessons();
        }
    );


// =====================================================
// BACK TO PDF
// =====================================================

document
    .getElementById("back-to-pdf")
    .addEventListener(
        "click",
        function () {

            hideAllSections();

            pdfSection.classList.remove(
                "hidden"
            );
        }
    );


// =====================================================
// START QUIZ
// =====================================================

async function startQuiz() {

    const quizButton =
        document.getElementById(
            "generate-quiz-button"
        );

    const status =
        document.getElementById(
            "quiz-status"
        );

    quizButton.disabled = true;

    quizButton.textContent =
        "Generating Quiz...";

    status.textContent =
        "Please wait while the AI generates your quiz.";

    try {

        const requestData = {

            subject:
                currentSubject.subject,

            course:
                currentCourse.course,

            lesson:
                currentLesson.lesson,

            number_of_questions: 5
        };

        console.log("================================");
        console.log("Generating Quiz");
        console.log(requestData);
        console.log("================================");

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
                        JSON.stringify(
                            requestData
                        )
                }
            );

        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(error);
        }

        const data =
            await response.json();

        console.log(
            "Quiz generated:",
            data
        );

        currentQuiz =
            data.quiz;

        currentQuizId =
            data.quiz_id;

        currentModel =
            data.route;

        displayQuiz();

    }
    catch (error) {

        console.error(
            "Quiz generation error:",
            error
        );

        status.textContent =
            "Failed to generate quiz.";

        alert(
            "Failed to generate quiz.\n\n" +
            error.message
        );

    }
    finally {

        quizButton.disabled = false;

        quizButton.textContent =
            "Generate Quiz";
    }
}


// =====================================================
// DISPLAY QUIZ
// =====================================================

function displayQuiz() {

    hideAllSections();

    quizSection.classList.remove("hidden");

    const container =
        document.getElementById(
            "quiz-container"
        );

    container.innerHTML = "";

    document
        .getElementById("quiz-description")
        .textContent =
            `${currentCourse.name} - ${currentLesson.name}`;

    currentQuiz.forEach(
        (question, index) => {

            const card =
                document.createElement("div");

            card.className =
                "question-card";

            let optionsHTML = "";

            question.options.forEach(
                option => {

                    optionsHTML += `

                        <label class="option">

                            <input
                                type="radio"
                                name="question-${index}"
                                value="${escapeHTML(option)}">

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
                    ${escapeHTML(
                        question.question
                    )}
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

document
    .getElementById("submit-quiz-button")
    .addEventListener(
        "click",
        submitQuiz
    );


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
            .getElementById("submit-status")
            .textContent =
                "Please answer all questions before submitting.";

        return;
    }


    document
        .getElementById("submit-status")
        .textContent =
            "Submitting quiz...";


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

    }
    catch (error) {

        console.error(error);

        document
            .getElementById("submit-status")
            .textContent =
                "Failed to submit quiz.";

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

    hideAllSections();

    resultSection.classList.remove(
        "hidden"
    );


    document
        .getElementById("result-quiz-id")
        .textContent =
            result.quiz_id ||
            currentQuizId;


    document
        .getElementById("result-progress-id")
        .textContent =
            result.progress_id ||
            "-";


    document
        .getElementById("result-ai-model")
        .textContent =
            currentModel ||
            "-";


    document
        .getElementById("result-score")
        .textContent =
            `${result.score} / ${result.total_questions}`;
}


// =====================================================
// RETURN TO LESSONS
// =====================================================

document
    .getElementById("return-to-lessons")
    .addEventListener(
        "click",
        function () {

            hideAllSections();

            lessonsSection.classList.remove(
                "hidden"
            );

            loadLessons();
        }
    );


// =====================================================
// HTML ESCAPE
// =====================================================

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value;

    return div.innerHTML;
}


// =====================================================
// INITIAL PAGE
// =====================================================

showSubjects();