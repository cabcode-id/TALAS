import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function SearchBar() { 
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const  handleKeyPress = (event) => {
    if (event.key === 'Enter' && searchQuery !== "") {
      navigate(`/search?q=${searchQuery}`);
    }
  };

  return (
    <input
      type="text"
      value={searchQuery}
      onChange={(e) =>  setSearchQuery(e.target.value)}
      placeholder="Search Anything"
      className="w-full h-full text-[#9F9F9F] rounded-lg bg-white p-2.5 pl-4 pr-10 outline-red-200 focus:ring-2 focus:ring-[#FF8585] focus:shadow-md transition delay-150 duration-300 ease-in-out outline-none"
      onKeyDown={handleKeyPress}
    />
  );
}

export default SearchBar;