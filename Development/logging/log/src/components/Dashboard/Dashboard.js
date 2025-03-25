import React, { useEffect, useRef } from "react";

export default function Dashboard() {
  // Use a ref to track if we've already logged this session
  const hasLogged = useRef(false);
  
  useEffect(() => {
    // Skip if we've already logged during this component lifecycle
    if (hasLogged.current) return;
    
    // Dapatkan token dari localstorage (kalau ada)
    const tokenString = localStorage.getItem("token");
    const tokenObject = tokenString ? JSON.parse(tokenString) : null;
    const token = tokenObject ? tokenObject.token : null;

    console.log("Token value:", token);

    if (token) {
      // mark sdh login (kalau ngga bisa kekirim double)
      hasLogged.current = true;
      
      const currentPageUrl = window.location.href;
      
      // fetch dari server.js
      fetch('http://localhost:8080/log', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: token,
          action: currentPageUrl,
        }),
      })
      .catch(error => console.error('Error logging page visit:', error));
    }
  }, []); 

  return <h2>Dashboard</h2>;
}
