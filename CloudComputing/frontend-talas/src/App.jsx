import './App.css';
import DarkModeToggle from './components/DarkModeToggle';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PageSwitch from "./components/PageSwitch"; // Impor komponen PageSwitch
import Navbar from './components/Navbar'; // Impor Navbar yang baru dipindahkan
import News from './components/News';
import ToggleGroup from './components/ToggleGroup';

export default function App() {
  return (
    <>
      <Router>
        <div>
          {/* Navbar dan DarkModeToggle akan selalu muncul di semua halaman */}
          <Navbar />
          <DarkModeToggle />

          {/* Routes menentukan halaman mana yang akan dimuat berdasarkan URL */}
          <Routes>
            {/* Route untuk Landing Page (berada di URL root "/") */}
            <Route 
              path="/" 
              element={
                <News />  
              } 
            />

            {/* Route untuk halaman Home dan PageSwitch */}
            <Route 
              path="/bias/*"  // Perhatikan penambahan '/*' di sini
              element={
                <>
                  <PageSwitch />
                  <ToggleGroup />
                </>
              } 
            />
          </Routes>
        </div>
      </Router>
    </>
  );
}
