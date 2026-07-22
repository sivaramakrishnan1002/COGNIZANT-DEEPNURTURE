/*
  ==========================================================================
  SIDE-BY-SIDE COMPARISON: FETCH vs AXIOS (Step 59)
  ==========================================================================
  1. Response Data Parsing:
     - Fetch: Requires manual call to .json() method (e.g., await response.json()).
     - Axios: Automatically parses JSON response data into response.data.

  2. Error Handling & HTTP Status Codes:
     - Fetch: Only rejects Promise on network failures. Doesn't reject on 404 or 500 status codes (requires manual response.ok check).
     - Axios: Automatically rejects Promise for any status codes outside the 2xx range (e.g. 404, 500).

  3. Built-in Features & Utility:
     - Fetch: Standard browser API; lacks built-in request interceptors, request timeout options, or request cancellation.
     - Axios: Provides request/response interceptors (axios.interceptors), built-in request cancellation, and configurable timeouts out-of-the-box.
  ==========================================================================
*/

const BASE_URL = 'https://jsonplaceholder.typicode.com';

// Local course dataset
const localCourses = [
    { id: 101, name: "Advanced Web Development", code: "CS201", credits: 4 },
    { id: 102, name: "Cloud Native Architecture", code: "CS202", credits: 4 },
    { id: 103, name: "Microservices & Containers", code: "CS203", credits: 3 }
];

// Step 45: Promise chaining fetch user by ID
function fetchUser(id) {
    console.log(`[Promise .then] Fetching user ${id}...`);
    return fetch(`${BASE_URL}/users/${id}`)
        .then(response => response.json())
        .then(user => {
            console.log(`[Promise .then Result] User Name: ${user.name}`);
            return user;
        })
        .catch(err => console.error("Error in fetchUser:", err));
}

// Step 46: Async/await fetch user by ID with try/catch
async function fetchUserAsync(id) {
    console.log(`[async/await] Fetching user ${id}...`);
    try {
        const response = await fetch(`${BASE_URL}/users/${id}`);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const user = await response.json();
        console.log(`[async/await Result] User Name: ${user.name}`);
        return user;
    } catch (error) {
        console.error("Error in fetchUserAsync:", error);
    }
}

// Step 47: Simulate 1-second network delay using new Promise
function fetchAllCourses() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(localCourses);
        }, 1000);
    });
}

// Step 48: Render courses only after promise resolves with loading state
async function loadCoursesWithDelay() {
    const loader = document.getElementById('course-loader');
    const grid = document.getElementById('course-grid');

    loader.style.display = 'flex';
    grid.innerHTML = '';

    const courses = await fetchAllCourses();

    loader.style.display = 'none';

    courses.forEach(c => {
        const card = document.createElement('article');
        card.className = 'course-card';
        card.innerHTML = `
            <h3>${c.name}</h3>
            <p>Code: ${c.code} | Credits: ${c.credits}</p>
        `;
        grid.appendChild(card);
    });
}

// Step 49: Demonstrate Promise.all() for simultaneous user requests
async function testPromiseAll() {
    const outputEl = document.getElementById('axios-output');
    outputEl.innerHTML = '<p>Running Promise.all(user 1, user 2)...</p>';

    try {
        const [user1, user2] = await Promise.all([
            fetch(`${BASE_URL}/users/1`).then(res => res.json()),
            fetch(`${BASE_URL}/users/2`).then(res => res.json())
        ]);

        console.log(`[Promise.all] User 1: ${user1.name}, User 2: ${user2.name}`);
        outputEl.innerHTML = `
            <p>✅ <strong>Promise.all Completed:</strong></p>
            <p>• User 1 Name: <strong>${user1.name}</strong></p>
            <p>• User 2 Name: <strong>${user2.name}</strong></p>
        `;
    } catch (error) {
        console.error("Promise.all failed:", error);
    }
}

// Step 50: Reusable apiFetch wrapper checking response.ok
async function apiFetch(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`API Request Failed: HTTP Status ${response.status} (${response.statusText || 'Not Found'})`);
    }
    return await response.json();
}

// Step 51 - 54: Fetch notifications with loader, error handling, and retry button
let lastAttemptedUrl = `${BASE_URL}/posts?_limit=4`;

async function loadNotifications(targetUrl = `${BASE_URL}/posts?_limit=4`) {
    lastAttemptedUrl = targetUrl;

    const loader = document.getElementById('notif-loader');
    const errorBanner = document.getElementById('notif-error-banner');
    const errorMsg = document.getElementById('error-message');
    const container = document.getElementById('notif-cards-container');

    // Step 52: Show spinner, hide errors and cards
    loader.style.display = 'flex';
    errorBanner.style.display = 'none';
    container.innerHTML = '';

    try {
        const posts = await apiFetch(targetUrl);

        loader.style.display = 'none';

        posts.forEach(post => {
            const card = document.createElement('div');
            card.className = 'notif-card';
            card.innerHTML = `
                <h4>📢 ${post.title.substring(0, 35)}...</h4>
                <p>${post.body.substring(0, 90)}...</p>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        // Step 53: Display user-friendly error message in UI
        loader.style.display = 'none';
        errorMsg.textContent = `❌ ${error.message}`;
        errorBanner.style.display = 'flex';
    }
}

// Step 58: Axios Request Interceptor
axios.interceptors.request.use(config => {
    console.log(`[Axios Interceptor] API call started: ${config.url}`);
    return config;
}, error => {
    return Promise.reject(error);
});

// Step 56 - 57: Axios GET request with params (userId: 1)
async function fetchUser1PostsAxios() {
    const outputEl = document.getElementById('axios-output');
    outputEl.innerHTML = '<p>Fetching User 1 posts via Axios with params...</p>';

    try {
        // Step 57: axios.get with params
        const response = await axios.get(`${BASE_URL}/posts`, {
            params: { userId: 1 }
        });

        console.log("[Axios Response Data]", response.data);

        const first3 = response.data.slice(0, 3);
        let html = `<p>✅ <strong>Axios Fetched ${response.data.length} Posts for User 1:</strong></p><ul>`;
        first3.forEach(p => {
            html += `<li><strong>${p.title.substring(0, 30)}...</strong></li>`;
        });
        html += '</ul>';

        outputEl.innerHTML = html;
    } catch (error) {
        console.error("Axios request error:", error);
        outputEl.innerHTML = `<p style="color:#ef4444">❌ Axios Error: ${error.message}</p>`;
    }
}

// Event Listeners setup
document.addEventListener('DOMContentLoaded', () => {
    // Step 45 & 46 test
    fetchUser(1);
    fetchUserAsync(2);

    // Step 48 initial load
    loadCoursesWithDelay();

    // Step 51 initial load
    loadNotifications(`${BASE_URL}/posts?_limit=4`);

    // UI Buttons
    document.getElementById('btn-load-posts').addEventListener('click', () => {
        loadNotifications(`${BASE_URL}/posts?_limit=4`);
    });

    document.getElementById('btn-sim-error').addEventListener('click', () => {
        // Step 53: Simulate 404 error
        loadNotifications(`${BASE_URL}/nonexistent-endpoint-404`);
    });

    // Step 54: Retry button handler
    document.getElementById('retry-btn').addEventListener('click', () => {
        loadNotifications(lastAttemptedUrl);
    });

    // Axios & Promise.all buttons
    document.getElementById('btn-axios-user1').addEventListener('click', fetchUser1PostsAxios);
    document.getElementById('btn-promise-all').addEventListener('click', testPromiseAll);
});
