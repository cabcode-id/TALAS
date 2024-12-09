// eslint-disable-next-line no-unused-vars
import React from "react";
import { Routes, Route, useParams } from 'react-router-dom';
import './PageSwitch.css';
import { newsData } from '../MockData'; // Pastikan path sesuai
import './Navbar.css';
import ToggleGroup from "./ToggleGroup";


// Komponen untuk menampilkan detail berita (hanya judul)
function NewsDetail() {
  const { id } = useParams(); // Mengambil ID berita dari URL
  const news = newsData.find(item => item.id === parseInt(id)); // Menemukan berita berdasarkan ID

  if (!news) {
    return <h2>Berita tidak ditemukan</h2>;
  }

  return (
    <div className="news-container">
      {/* Kolom Kiri */}
      <div className="left-column">
        <h1 className="detail-title">{news.title}</h1> {/* Menampilkan judul berita */}
        <ToggleGroup newsId={news.id} />
      </div>

      {/* Kolom Kanan (opsional, bisa digunakan untuk konten lain) */}
      <div className="right-column">
        <p>Informasi tambahan atau widget lainnya </p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
      </div>
    </div>
  );
}

// PageSwitch: Routing untuk menampilkan Detail berita
function PageSwitch() {
  return (
    <div className="page-switch">
    <Routes>
      {/* Menampilkan detail berita dengan parameter ID */}
      <Route path="/:id" element={<NewsDetail />} />
    </Routes>
    </div>
  );
}

export default PageSwitch;