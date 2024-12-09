import './App.css';
import DarkModeToggle from './components/DarkModeToggle';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PageSwitch from "./components/PageSwitch";
import Navbar from './components/Navbar';
import FormLogin from './components/FormLogin';
import News from './components/News';
import ToggleMenu from './components/ToggleMenu';
// import About from './pages/About';
import About from './pages/about';

export default function App() {
  return (
    <Router>
      <div>
        {/* Navbar dan DarkModeToggle selalu muncul di semua halaman */}
        <Navbar />
        <DarkModeToggle />

        {/* Routes menentukan halaman berdasarkan URL */}
        <Routes>
          <Route 
            path="/" 
            element={
              <>
                <News />
                <ToggleMenu />
              </>
            } 
          />
          <Route path="/bias/*" element={<PageSwitch />} />
          <Route path="/login" element={<FormLogin />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </Router>
  );
}