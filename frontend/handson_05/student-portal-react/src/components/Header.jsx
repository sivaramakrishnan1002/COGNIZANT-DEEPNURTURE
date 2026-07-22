import React from 'react';

// Task 1 (Step 62 & 64) & Task 2 (Step 70): Header component receiving siteName and enrolledCount props
export default function Header(props) {
  return (
    <header className="app-header">
      <div className="site-logo">
        {/* Step 64: Display siteName from props */}
        <h2>{props.siteName}</h2>
      </div>
      <nav className="header-nav">
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#courses">Courses</a></li>
          <li><a href="#profile">Profile</a></li>
        </ul>
      </nav>
      {/* Step 70: Display enrolled count badge */}
      <div className="enrolled-badge">
        🎓 Enrolled: <strong>{props.enrolledCount || 0}</strong>
      </div>
    </header>
  );
}
