// eslint-disable-next-line no-unused-vars
import React, { useState } from 'react';
import './ToggleMenu.css'; // pastikan Anda membuat file CSS yang sesuai
import './Navbar.css'; 

function Menu() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  return (
    <nav className="menu">
      {/* Checkbox untuk toggle */}
      <input
        id="menu__toggle"
        type="checkbox"
        className="menu__toggle"
        checked={isMenuOpen}
        onChange={toggleMenu}
      />
      <label htmlFor="menu__toggle" className="menu__toggle-label">
        <svg preserveAspectRatio="xMinYMin" viewBox="0 0 24 24">
          <path d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z" />
        </svg>
        <svg
          preserveAspectRatio="xMinYMin"
          viewBox="0 0 24 24"
          className={isMenuOpen ? 'open' : ''}
        >
          <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
        </svg>
      </label>

      {/* Konten menu */}
      <ol className={`menu__content ${isMenuOpen ? 'open' : ''}`}>
        <li className="menu-item">
          <a href="#0">Home</a>
        </li>
        <li className="menu-item">
          <a href="#0">My Account</a>
        </li>
        <li className="menu-item">
          <a href="#0">Sing Out</a>
        </li>
        <li className="menu-item">
          <a href="#0">About Talas</a>
          {/* <ol className="sub-menu">
            <li className="menu-item">
              <a href="#0">Big Widgets</a>
            </li>
            <li className="menu-item">
              <a href="#0">Bigger Widgets</a>
            </li>
            <li className="menu-item">
              <a href="#0">Huge Widgets</a>
            </li>
          </ol> */}
        </li>
        <li className="menu-item">
          <a href="#0">Subscribe</a>
          {/* <ol className="sub-menu">
            <li className="menu-item">
              <a href="#0">Shishkabobs</a>
            </li>
            <li className="menu-item">
              <a href="#0">BBQ kabobs</a>
            </li>
            <li className="menu-item">
              <a href="#0">Summer kabobs</a>
            </li>
          </ol> */}
        </li>
        <li className="menu-item">
          <a href="#0">Website Settings</a>
        </li>
        <li className="menu-item">
          <a href="#0">Contact Us</a>
        </li>
        <li className="menu-item">
          <a href="#0">International Politics</a>
        </li>
        <li className="menu-item">
          <a href="#0">Finance</a>
        </li>
        <li className="menu-item">
          <a href="#0">Science & Tech</a>
        </li>
        <li className="menu-item">
          <a href="#0">Referral Code</a>
        </li>
        <li className="menu-item">
          <a href="#0">International</a>
        </li>
        <li className="menu-item">
          <a href="#0">Discover More Topic</a>
        </li>
        <li className="menu-item">
          <a href="#0">Product</a>
        </li>
        <li className="menu-item">
          <a href="#0">Suggest a Source</a>
        </li>
      </ol>
    </nav>
  );
}

export default Menu;
