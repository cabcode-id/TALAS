// eslint-disable-next-line no-unused-vars
import React from "react";
import { Routes, Route, useParams } from 'react-router-dom';
import './PageSwitch.css';
import { newsData } from '../MockData'; // Pastikan path sesuai
import './Navbar.css';


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
      </div>

      {/* Kolom Kanan (opsional, bisa digunakan untuk konten lain) */}
      <div className="right-column">
        <p>Informasi tambahan atau widget lainnya</p>
      </div>
    </div>
  );
}

// PageSwitch: Routing untuk menampilkan Detail berita
function PageSwitch() {
  return (
    <Routes>
      {/* Menampilkan detail berita dengan parameter ID */}
      <Route path="/:id" element={<NewsDetail />} />
    </Routes>
  );
}

export default PageSwitch;