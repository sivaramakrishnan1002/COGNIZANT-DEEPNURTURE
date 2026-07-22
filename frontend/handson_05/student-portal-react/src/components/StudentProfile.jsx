import React, { useState } from 'react';

// Task 3 (Step 74): StudentProfile component with local state (name, email, semester)
export default function StudentProfile() {
  const [profile, setProfile] = useState({
    name: 'Alex Johnson',
    email: 'alex.johnson@student.edu',
    semester: 'Semester 6'
  });

  const [savedMessage, setSavedMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSavedMessage('Profile updated successfully!');
    setTimeout(() => setSavedMessage(''), 3000);
  };

  return (
    <section className="profile-section" id="profile">
      <h2>Student Profile</h2>
      {savedMessage && <div className="success-banner">{savedMessage}</div>}
      <form onSubmit={handleSubmit} className="profile-form">
        <div className="form-group">
          <label htmlFor="name">Full Name</label>
          <input 
            type="text" 
            id="name" 
            name="name" 
            value={profile.name} 
            onChange={handleChange} 
            required 
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input 
            type="email" 
            id="email" 
            name="email" 
            value={profile.email} 
            onChange={handleChange} 
            required 
          />
        </div>

        <div className="form-group">
          <label htmlFor="semester">Current Semester</label>
          <select 
            id="semester" 
            name="semester" 
            value={profile.semester} 
            onChange={handleChange}
          >
            <option value="Semester 1">Semester 1</option>
            <option value="Semester 2">Semester 2</option>
            <option value="Semester 3">Semester 3</option>
            <option value="Semester 4">Semester 4</option>
            <option value="Semester 5">Semester 5</option>
            <option value="Semester 6">Semester 6</option>
            <option value="Semester 7">Semester 7</option>
            <option value="Semester 8">Semester 8</option>
          </select>
        </div>

        <button type="submit" className="save-btn">Save Profile Changes</button>
      </form>
    </section>
  );
}
