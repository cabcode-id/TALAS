// eslint-disable-next-line no-unused-vars
import React from "react";
// import './PageSwitch.css';
import './About.css';



// Komponen untuk menampilkan detail berita (hanya judul)
function About() {

  return (
    <div className="container-about">
      {/* Kolom Kanan (opsional, bisa digunakan untuk konten lain) */}
      <div >
        <p className="text-about">Informasi tambahan atau widget lainnya </p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
      </div>
    </div>
  );
}


export default About;