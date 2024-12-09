// eslint-disable-next-line no-unused-vars
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Jika ada file CSS khusus untuk Navbar
import ToggleMenu from './ToggleMenu';



// eslint-disable-next-line react/prop-types
function Navbar({ onLoginClick }) {
  return (
    <nav className="navbar">
      <ToggleMenu />    
      <Logo />
      <Search />
      <Button onClick={onLoginClick} />
    </nav>
  );
}

function Logo() {
  return (
    <div className="logo-container">
      <img src="/Title.png" alt="Title" className="title" />
    </div>
  );
}

function Search() {
  const [query, setQuery] = useState('');
  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search..."
        className="search-bar"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
    </div>
  );
}

// eslint-disable-next-line react/prop-types
function Button({ onLoginClick }) {
  return (
    <div className="auth-buttons">
      
      <Link to="/login"> 
      <button onClick={onLoginClick} className="btn login-btn">Login</button>
      </Link>
      <button className="btn subscribe-btn">Subscribe</button>
    </div>
  );
}

export default Navbar;