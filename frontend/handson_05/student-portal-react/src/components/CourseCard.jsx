import React from 'react';

// Task 1 (Step 65) & Task 2 (Step 69): CourseCard component
export default function CourseCard({ id, name, code, credits, grade, isEnrolled, onEnroll }) {
  return (
    <article className={`course-card ${isEnrolled ? 'enrolled' : ''}`}>
      <h3>{name}</h3>
      <p className="course-code">{code}</p>
      <div className="course-details">
        <span className="credits-badge">{credits} Credits</span>
        <span className="grade-badge">Grade: {grade}</span>
      </div>
      {/* Step 69: Add Enroll button and trigger handler */}
      <button 
        className={`enroll-btn ${isEnrolled ? 'btn-enrolled' : ''}`}
        disabled={isEnrolled}
        onClick={() => onEnroll({ id, name, code, credits, grade })}
      >
        {isEnrolled ? '✓ Enrolled' : 'Enroll Course'}
      </button>
    </article>
  );
}
