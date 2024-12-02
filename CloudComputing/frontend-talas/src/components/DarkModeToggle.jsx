import { useState, useEffect } from 'react';
import './DarkModeToggle.css';

function DarkModeToggle() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Menggunakan useEffect untuk menambahkan/removal class 'dark' pada body
  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('dark');  // Menambahkan class dark ke body
    } else {
      document.body.classList.remove('dark'); // Menghapus class dark dari body
    }
  }, [isDarkMode]);

  const toggleMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div className="flex justify-center items-center vh-100">
      <div className={`element flex flex-wrap items-center ${isDarkMode ? 'active' : ''}`}>
        <div className="checkbox-wrap">
          <input
            type="checkbox"
            className="toggle-switch"
            checked={isDarkMode}
            onChange={toggleMode}
          />
        </div>
        <div className="opts">
          <div className="opt-1">
            <p>light mode</p>
          </div>
          <div className="opt-2">
            <p>dark mode</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DarkModeToggle;
