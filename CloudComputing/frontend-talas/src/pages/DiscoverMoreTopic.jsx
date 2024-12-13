// eslint-disable-next-line no-unused-vars
import React, { useState, useEffect } from "react";
// import { Link } from 'react-router-dom';
import './DiscoverMoreTopic.css';

// Komponen untuk menampilkan detail berita (hanya judul)
function Discover() {
  const [news, setNews] = useState([]); // Untuk menyimpan data berita dari API
  const [error, setError] = useState(null); // Untuk menangani error
  const [message, setMessage] = useState(''); // Menyimpan pesan untuk h1
  const baseUrl = import.meta.env.VITE_BASE_URL; // Ambil baseUrl dari environment variable

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await fetch(`${baseUrl}/news`); // Ganti dengan endpoint yang sesuai
        if (!response.ok) {
          throw new Error("Failed to fetch news data.");
        }
        const data = await response.json(); // Ambil data dalam format JSON
        setNews(data); // Simpan data ke state

        // Set pesan berdasarkan data atau logika tertentu
        if (data.length > 0) {
          setMessage("Discover Latest News"); // Menampilkan pesan jika ada berita
        } else {
          setMessage("No news available at the moment"); // Jika tidak ada berita
        }
      } catch (err) {
        setError(err.message); // Tangani error jika ada
      }
    };

    fetchNews(); // Panggil fungsi untuk mengambil data berita
  }, [baseUrl]);

  if (error) {
    return <div>Error: {error}</div>; // Tampilkan error jika ada
  }

  if (!news.length) {
    return <div>Loading...</div>; // Tampilkan loading jika data belum ada
  }

  return (
    <div className="container-discover">
      <div className="left-discover">
        <h1 className="h1">{message}</h1> {/* Menampilkan pesan */}
        {news.slice(0, 5).map((newsItem) => (
          <div className="left-container" key={newsItem.id}>
            <section className="title-discover">
              <img src={newsItem.imageUrl} alt={newsItem.title} className="img" />
             
            </section>
          </div>
        ))}
      </div>

      <div className="right-discover-2">
        {news.slice(0, 5).map((newsItem) => (
          <div className="right-container" key={newsItem.id}>
            <section className="title-discover">
              <img src={newsItem.imageUrl} alt={newsItem.title} className="img" />
             
            </section>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Discover;
