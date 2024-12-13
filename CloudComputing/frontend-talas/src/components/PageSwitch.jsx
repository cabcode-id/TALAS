

// eslint-disable-next-line no-unused-vars
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import './PageSwitch.css';
import './Navbar.css';
import ToggleGroup from "./ToggleGroup";
import { Routes, Route } from 'react-router-dom'; // Pastikan ini ada


const BASE_URL = import.meta.env.VITE_BASE_URL;  // Mengambil base URL dari environment variables

// Komponen untuk menampilkan detail berita (hanya judul)
function NewsDetail() {
  const { id } = useParams(); // Mengambil ID berita dari URL
  const [news, setNews] = useState(null); // State untuk menyimpan data berita
  const [loading, setLoading] = useState(true); // State untuk menangani loading
  const [error, setError] = useState(null); // State untuk menangani error

  // Fetch data berita berdasarkan ID dari API
  useEffect(() => {
    const fetchNewsDetail = async () => {
      try {
        const response = await fetch(`${BASE_URL}/article/${id}`); // Mengambil berita berdasarkan ID
        if (!response.ok) {
          throw new Error("Berita tidak ditemukan");
        }
        const data = await response.json();
        setNews(data);  // Set data berita ke state
      } catch (error) {
        setError(error.message);  // Tangani error
      } finally {
        setLoading(false);  // Set loading ke false setelah selesai
      }
    };

    fetchNewsDetail();
  }, [id]); // Efek ini akan dijalankan setiap kali ID berubah

  if (loading) return <h2>Loading...</h2>;
  if (error) return <h2>{error}</h2>;

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
        <p>{news.content || "Informasi tambahan atau widget lainnya"}</p>
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
