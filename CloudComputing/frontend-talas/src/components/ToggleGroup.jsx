import { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import { newsData } from '../MockData';  // Mengimpor data berita dari mockData
import styles from "./ToggleGroup.module.css"; // Mengimpor file CSS Module
import './PageSwitch.css';

function ToggleGroup({ newsId }) {
  const [colorationLevel, setColorationLevel] = useState("center");
  const [selectedNewsId, setSelectedNewsId] = useState(newsId); // Gunakan newsId sebagai default

  useEffect(() => {
    setSelectedNewsId(newsId); // Perbarui ID berita ketika props newsId berubah
  }, [newsId]);

  const handleChange = (event) => {
    setColorationLevel(event.target.value);
  };

  // Fungsi untuk mengambil summary berdasarkan ID berita dan level
  const getSummary = () => {
    const selectedNews = newsData.find(news => news.id === selectedNewsId); // Temukan berita berdasarkan ID
    if (!selectedNews) return 'Pilih berita terlebih dahulu.';

    switch (colorationLevel) {
      case "left":
        return selectedNews.left;
      case "center":
        return selectedNews.center;
      case "right":
        return selectedNews.right;
      default:
        return 'Pilih salah satu untuk melihat summary.';
    }
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
