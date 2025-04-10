import { useState} from "react";
import { Menu, X, ChevronDown } from "lucide-react"; 
import { Link } from "react-router-dom";
import SearchBar from "./SearchBar";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  return (
    <nav className="bg-[#FFD7CF] h-28 w-full">
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 h-full">
        <div className="relative flex h-full items-center justify-between">
          {/* Logo & Desktop Nav */}
          <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
            <div className="flex shrink-0 items-center">
              <a href="/home">
                <img className="h-10 w-auto" src="/Talas.svg" alt="Talas Logo" />
              </a>
            </div>
            <div className="hidden sm:ml-6 sm:block">
              <div className="flex space-x-4">
                <a href="/home" className="rounded-md px-3 py-2 text-base font-medium text-black hover:bg-gray-700 hover:text-white">Home</a>
                <div className="relative">
                    <button
                        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                        className="flex items-center gap-1 rounded-md px-3 py-2 text-base font-medium text-black hover:bg-gray-700 hover:text-white"
                    >
                        Categories
                        <ChevronDown size={16} />
                    </button>
                    {isDropdownOpen && (
                        <div className="absolute left-0 mt-2 w-40 bg-white rounded-md shadow-lg z-10">
                            <Link to="#" className="block px-4 py-2 text-sm text-black hover:bg-gray-100">Tech</Link>
                            <Link to="#" className="block px-4 py-2 text-sm text-black hover:bg-gray-100">Lifestyle</Link>
                            <Link to="#" className="block px-4 py-2 text-sm text-black hover:bg-gray-100">News</Link>
                        </div>
                    )}
                </div>
                <a href="\about-us" className="rounded-md px-3 py-2 text-base font-medium text-black hover:bg-gray-700 hover:text-white">About Us</a>
              </div>
            </div>
          </div>

          {/* Hamburger button (mobile only) */}
          <div className="sm:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center rounded-md p-2 text-black hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
            >
              <span className="sr-only">Open main menu</span>
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>

          {/* Right Section */}
          <div className="hidden sm:flex items-center gap-4">
            <SearchBar />
            
            <a href="\subscription" className="p-2.5 px-6 bg-[#FF8585] text-white rounded-lg hover:bg-[#392c2c]">Subscribe</a>
            <a href="\login" className="p-2.5 px-9 bg-white text-[#FF8585] rounded-lg outline-[#FF8585] hover:bg-[#392c2c] hover:text-white">Login</a>

            {/* Toggle */}
            <div>
              <input type="checkbox" className="peer sr-only opacity-0" id="toggle" />
              <label htmlFor="toggle" className="relative flex h-11 w-6 cursor-pointer rounded-full bg-gray-400 px-0.5 outline-gray-400 transition-colors before:absolute before:top-[0.10rem] before:left-0.5 before:h-5 before:w-5 before:rounded-full before:bg-white before:shadow before:transition-transform before:duration-300 before:translate-y-0 peer-checked:bg-green-500 peer-checked:before:translate-y-full peer-focus-visible:outline peer-focus-visible:outline-offset-2 peer-focus-visible:outline-gray-400 peer-checked:peer-focus-visible:outline-green-500">
                <span className="sr-only">Enable</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="sm:hidden px-2 pb-3 pt-2 space-y-1">
          <a href="#" className="block rounded-md px-3 py-2 text-base font-medium text-black hover:bg-gray-700 hover:text-white">Home</a>
          <a href="#" className="block rounded-md px-3 py-2 text-base font-medium text-black hover:bg-gray-700 hover:text-white">Categories</a>
          <a href="#" className="block rounded-md px-3 py-2 text-base font-medium text-black hover:bg-gray-700 hover:text-white">About Us</a>
          <a href="#" className="block rounded-md px-3 py-2 text-base font-medium text-black hover:bg-gray-700 hover:text-white">Login</a>
        </div>
      )}
    </nav>
  );
}


export default Navbar;