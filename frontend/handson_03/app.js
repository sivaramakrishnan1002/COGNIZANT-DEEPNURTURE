// Step 30: Import array using ES6 import
import { courses } from './data.js';

let currentCourses = [...courses];

// Step 30: Use destructuring to extract name and credits from each course in a loop
console.log("--- Course Destructuring Loop ---");
currentCourses.forEach(course => {
    const { name, credits } = course;
    console.log(`Course Name: ${name}, Credits: ${credits}`);
});

// Step 31: Use Array.map() to create new array of strings formatted as 'CS101 — Data Structures (4 credits)'
const formattedCourses = currentCourses.map(c => `${c.code} — ${c.name} (${c.credits} credits)`);
console.log("--- Formatted Courses (Array.map) ---", formattedCourses);

// Step 32: Use Array.filter() to get only courses with credits >= 4. Log the count.
const highCreditCourses = currentCourses.filter(c => c.credits >= 4);
console.log(`--- High Credit Courses Count (credits >= 4): ${highCreditCourses.length} ---`);

// Step 33: Use Array.reduce() to calculate total credits enrolled. Log the result.
const totalCredits = currentCourses.reduce((acc, c) => acc + c.credits, 0);
console.log(`--- Total Credits Enrolled (Array.reduce): ${totalCredits} ---`);

// Step 36: DOM selection
const courseGrid = document.querySelector('.course-grid');
const totalCreditsEl = document.getElementById('total-credits');
const searchInput = document.getElementById('search-courses');
const sortBtn = document.getElementById('sort-credits-btn');
const selectedCourseBadge = document.getElementById('selected-course');

// Step 34 & Step 37-39: Render course cards using arrow function & template literal
const renderCourses = (courseArray) => {
    courseGrid.innerHTML = '';

    courseArray.forEach(course => {
        const { id, name, code, credits, grade } = course;
        
        // Step 37: Create article element and set innerHTML using template literal
        const article = document.createElement('article');
        article.className = 'course-card';
        article.dataset.id = id;
        article.dataset.name = name;
        article.dataset.grade = grade;

        article.innerHTML = `
            <h3>${name}</h3>
            <div class="code">${code}</div>
            <div class="meta">
                <span class="credits">${credits} Credits</span>
                <span class="grade">Grade: ${grade}</span>
            </div>
        `;

        // Step 38: Append created article to grid
        courseGrid.appendChild(article);
    });

    // Step 39: Update total credits paragraph dynamically
    const currentTotal = courseArray.reduce((acc, c) => acc + c.credits, 0);
    totalCreditsEl.textContent = `Total Enrolled Credits: ${currentTotal}`;
};

// Initial Render
renderCourses(currentCourses);

// Step 41: Search input event listener on 'input' event
searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    const filtered = courses.filter(c => c.name.toLowerCase().includes(query) || c.code.toLowerCase().includes(query));
    renderCourses(filtered);
});

// Step 42: Sort by Credits button handler (descending)
sortBtn.addEventListener('click', () => {
    const sorted = [...currentCourses].sort((a, b) => b.credits - a.credits);
    renderCourses(sorted);
});

// Step 44: Event delegation on .course-grid container
courseGrid.addEventListener('click', (event) => {
    const card = event.target.closest('.course-card');
    if (card) {
        const name = card.dataset.name;
        const grade = card.dataset.grade;

        // Step 43: Update UI & show selected course info
        selectedCourseBadge.style.display = 'block';
        selectedCourseBadge.textContent = `Selected Course: ${name} (Grade: ${grade})`;
    }
});
