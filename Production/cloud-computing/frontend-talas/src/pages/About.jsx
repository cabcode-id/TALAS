// eslint-disable-next-line no-unused-vars
import React, { useState, useEffect } from "react";
import './About.css';

function About() {
  const [data, setData] = useState(null); // Untuk menyimpan data yang diterima dari API
  const [error, setError] = useState(null); // Untuk menangani error
  const baseUrl = import.meta.env.VITE_BASE_URL; // Pastikan baseUrl diambil dari environment variable

  useEffect(() => {
    // Fungsi untuk mengambil data dari API
    const fetchData = async () => {
      try {
        const response = await fetch(`${baseUrl}/about`); // Ganti dengan endpoint API yang sesuai
        if (!response.ok) {
          throw new Error('Something went wrong'); // Tangani error jika response tidak berhasil
        }
        const result = await response.json(); // Ambil data JSON dari response
        setData(result); // Simpan data ke state
      } catch (err) {
        setError(err.message); // Tangani error dengan menampilkan pesan error
      }
    };

    fetchData(); // Panggil fungsi untuk mengambil data
  }, [baseUrl]); // Memanggil useEffect hanya ketika baseUrl berubah

  if (error) {
    return <div>Error: {error}</div>; // Tampilkan error jika ada
  }

  if (!data) {
    return <div>Loading...</div>; // Tampilkan loading jika data belum ada
  }

  return (
    <div className="container-about">
      <div>
        <p className="text-about">Informasi tambahan atau widget lainnya</p>
        {/* Menampilkan data yang diterima dari API */}
        <p>{data.description}</p> {/* Misalnya, jika data mengandung field 'description' */}
      </div>
    </div>
  );
}

export default About;
