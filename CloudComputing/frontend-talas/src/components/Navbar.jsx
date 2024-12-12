// eslint-disable-next-line no-unused-vars
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Jika ada file CSS khusus untuk Navbar
import ToggleMenu from './ToggleMenu';
// import { IoSearch } from "react-icons/io5";
// import { FaSearch } from "react-icons/fa";
// import { IoSearch } from "react-icons/io5";


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
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    console.log("Search query:", query);
  };

  return (
    <div className="search-bar-container">
      <input
        type="text"
        placeholder="Telusuri Talas.com"
        className="search-input"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button className="search-button" onClick={handleSearch}>
        <svg
          className="search-icon"
          // stroke="black"
          // fill="black"
          viewBox="0 0 512 512"
          height="33px"
          width="33px"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"
            style={{ fill: 'black', stroke: 'black' }} 
          ></path>
        </svg>
      </button>
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