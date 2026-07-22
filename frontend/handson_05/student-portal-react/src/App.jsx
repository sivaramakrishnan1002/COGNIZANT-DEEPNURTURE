import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseCard from './components/CourseCard';
import StudentProfile from './components/StudentProfile';

export default function App() {
  // Task 2 (Step 66): State for courses, search term, and enrolled courses
  const [courses, setCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  
  // Task 3 (Step 72 & 73): Loading and error states
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Task 3 (Step 71): useEffect fetching courses from JSONPlaceholder /posts on mount
  useEffect(() => {
    async function fetchCourses() {
      try {
        setLoading(true);
        const response = await fetch('https://jsonplaceholder.typicode.com/posts');
        if (!response.ok) throw new Error(`HTTP Error ${response.status}`);
        const posts = await response.json();

        // Map first 5 posts to course-like objects
        const mappedCourses = posts.slice(0, 5).map(post => ({
          id: post.id,
          name: post.title.charAt(0).toUpperCase() + post.title.slice(1, 28) + '...',
          code: `CS${100 + post.id}`,
          credits: (post.id % 3) + 3, // Generates 3 or 4 credits
          grade: ['A', 'A-', 'B+', 'B', 'A'][post.id % 5]
        }));

        setCourses(mappedCourses);
        setError(null);
      } catch (err) {
        setError(`Failed to load courses from API: ${err.message}`);
      } finally {
        setLoading(false);
      }
    }

    fetchCourses();
  }, []); // Empty dependency array means this effect runs once after initial mount

  /* 
    Task 3 (Step 75): useEffect with dependency array monitoring [courses] state.
    EXPLANATION OF DEPENDENCY ARRAY:
    The dependency array tells React when to re-execute this effect function.
    - If omitted altogether, the effect runs after EVERY single render, causing performance degradation or infinite loops.
    - If set to empty [], it runs only once when the component mounts.
    - Here, passing [courses] ensures the effect executes ONLY when the `courses` state variable is updated or changed.
  */
  useEffect(() => {
    if (courses.length > 0) {
      console.log('Courses state updated:', courses);
    }
  }, [courses]);

  // Task 2 (Step 69): Lift state up handler for course enrollment
  const handleEnroll = (course) => {
    if (!enrolledCourses.some(c => c.id === course.id)) {
      setEnrolledCourses(prev => [...prev, course]);
    }
  };

  // Task 2 (Step 68): Filter displayed courses based on search term
  const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="app-container">
      {/* Task 1 (Step 64) & Task 2 (Step 70): Header with props */}
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />

      <main className="main-content">
        <section className="hero-banner">
          <h1>Welcome to Student Course Hub</h1>
          <p>Explore interactive React components, dynamic state management, and API lifecycle hooks.</p>
        </section>

        <section className="courses-section" id="courses">
          <h2>Available Courses</h2>

          {/* Task 2 (Step 68): Search input */}
          <div className="search-bar">
            <input 
              type="text" 
              placeholder="Search courses by title or course code..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Task 3 (Step 72): Loading state display */}
          {loading && (
            <div className="loader">
              <div className="spinner"></div>
              <p>Loading courses from JSONPlaceholder API...</p>
            </div>
          )}

          {/* Task 3 (Step 73): Error state display */}
          {error && (
            <div className="error-message">
              <p>⚠️ {error}</p>
            </div>
          )}

          {/* Task 2 (Step 67): Map over courses state */}
          {!loading && !error && (
            <div className="course-grid">
              {filteredCourses.length > 0 ? (
                filteredCourses.map(course => (
                  <CourseCard 
                    key={course.id}
                    {...course}
                    isEnrolled={enrolledCourses.some(c => c.id === course.id)}
                    onEnroll={handleEnroll}
                  />
                ))
              ) : (
                <p className="no-results">No courses match your search criteria "{searchTerm}".</p>
              )}
            </div>
          )}
        </section>

        {/* Task 3 (Step 74): Student Profile component */}
        <StudentProfile />
      </main>

      {/* Task 1 (Step 63): Footer component */}
      <Footer />
    </div>
  );
}
