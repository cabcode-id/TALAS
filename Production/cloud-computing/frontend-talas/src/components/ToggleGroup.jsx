import { useState, useEffect } from "react";
import './ToggleGroup.module.css'; // Pastikan file CSS sesuai
import styles from "./ToggleGroup.module.css"; // Mengimpor file CSS Module

// eslint-disable-next-line react/prop-types
function ToggleGroup({ newsId }) {
  const [colorationLevel, setColorationLevel] = useState("center");
  const [selectedNewsId, setSelectedNewsId] = useState(newsId); // Gunakan newsId sebagai default
  const [news, setNews] = useState(null); // Menyimpan berita yang diambil dari API
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Memperbarui newsId ketika props newsId berubah
  useEffect(() => {
    setSelectedNewsId(newsId);
  }, [newsId]);

  // Mengambil data berita berdasarkan ID dari API
  useEffect(() => {
    const fetchNews = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${import.meta.env.VITE_BASE_URL}/article/${selectedNewsId}`);
        if (!response.ok) throw new Error("Data tidak ditemukan");
        const data = await response.json();
        setNews(data); // Menyimpan data berita di state
      } catch (error) {
        setError(error.message); // Menangani error
      } finally {
        setLoading(false);
      }
    };

    if (selectedNewsId) {
      fetchNews();
    }
  }, [selectedNewsId]);

  // Mengambil summary berdasarkan level
  const getSummary = () => {
    if (loading) return 'Loading...'; // Tampilkan loading jika data masih diambil
    if (error) return `Error: ${error}`; // Tampilkan error jika ada masalah dengan fetch

    if (!news) return 'Pilih berita terlebih dahulu.'; // Jika berita tidak ditemukan

    switch (colorationLevel) {
      case "left":
        return news.left;  // Gunakan data dari API
      case "center":
        return news.center;  // Gunakan data dari API
      case "right":
        return news.right;  // Gunakan data dari API
      default:
        return 'Pilih salah satu untuk melihat summary.';
    }
  };

  // Mengubah state colorationLevel ketika pilihan radio berubah
  const handleChange = (event) => {
    setColorationLevel(event.target.value);
  };

  return (
    <div className="toggle-container">
      <div className={styles.hiddenToggles}>
        {/* Left Button */}
        <input
          name="coloration-level"
          type="radio"
          id="coloration-left"
          value="left"
          className={styles.hiddenToggles__input}
          checked={colorationLevel === "left"}
          onChange={handleChange}
        />
        <label
          htmlFor="coloration-left"
          className={`${styles.hiddenToggles__label} ${colorationLevel === "left" ? styles.leftActive : ""}`}
        >
          Left
        </label>

        {/* Center Button */}
        <input
          name="coloration-level"
          type="radio"
          id="coloration-center"
          value="center"
          className={styles.hiddenToggles__input}
          checked={colorationLevel === "center"}
          onChange={handleChange}
        />
        <label
          htmlFor="coloration-center"
          className={`${styles.hiddenToggles__label} ${colorationLevel === "center" ? styles.centerActive : ""}`}
        >
          Center
        </label>

        {/* Right Button */}
        <input
          name="coloration-level"
          type="radio"
          id="coloration-right"
          value="right"
          className={styles.hiddenToggles__input}
          checked={colorationLevel === "right"}
          onChange={handleChange}
        />
        <label
          htmlFor="coloration-right"
          className={`${styles.hiddenToggles__label} ${colorationLevel === "right" ? styles.rightActive : ""}`}
        >
          Right
        </label>
      </div>

      <div className="summary">
        <p>{getSummary()}</p> {/* Menampilkan summary berdasarkan pilihan toggle */}
      </div>
    </div>
  );
}

export default ToggleGroup;
