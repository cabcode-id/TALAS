import './App.css';
import DarkModeToggle from './components/DarkModeToggle';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PageSwitch from "./components/PageSwitch";
import Navbar from './components/Navbar';
import FormLogin from './components/FormLogin';
import News from './components/News';
import ToggleMenu from './components/ToggleMenu';
import About from './pages/About';
import Finance from "./pages/Finance";
// import Footer from "./components/Footer"
import International from "./pages/International";
import Science from './pages/Science';
import Discover from './pages/DiscoverMoreTopic';
export default function App() {
  return (
    <Router>
      <div>
        {/* Navbar dan DarkModeToggle selalu muncul di semua halaman */}
        <Navbar />
        <DarkModeToggle />
        
        {/* <Finance/> */}

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
          <Route path="/finance" element={<Finance />} />
          <Route path="/international" element={<International />} />
          <Route path="/science" element={<Science />} />
          <Route path="/discover" element={<Discover/>} />
          {/* <Route path="/finance" element={<Finance />} />
          <Route path="/finance" element={<Finance />} /> */}
        </Routes>

        {/* <Footer /> */}
      </div>
    </Router>
  );
}