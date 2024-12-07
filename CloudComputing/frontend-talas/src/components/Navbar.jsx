// eslint-disable-next-line no-unused-vars
import React, { useState } from 'react';
import './Navbar.css'; // Jika ada file CSS khusus untuk Navbar
import ToggleMenu from './ToggleMenu';



function Navbar() {
  return (
    <nav className="navbar">
      <ToggleMenu />    
      <Logo />
      <Search />
      <Button />
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

function Button() {
  return (
    <div className="auth-buttons">
      <button className="btn login-btn">Login</button>
      <button className="btn subscribe-btn">Subscribe</button>
    </div>
  );
}

export default Navbar;
