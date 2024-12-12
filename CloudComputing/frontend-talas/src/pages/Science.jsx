
// eslint-disable-next-line no-unused-vars
import React from "react";
import { Link } from 'react-router-dom';
import { newsData } from '../MockData';

// import './PageSwitch.css';
import './Science.css';


// Komponen untuk menampilkan detail berita (hanya judul)
function Science() {

  return (
    <div className="container-science">
      {/* Kolom Kanan (opsional, bisa digunakan untuk konten lain) */}
      <div className="left-science">
        
      <h1 className="h1">Science</h1>
      {newsData.slice(0,5).map((news) => ( // Menampilkan 3 berita pertama
        <div className="left-container" key={news.id}>
            <section className="title-science">
              <img src={news.imageUrl} alt={news.title} className="img" />
              <article>
              <Link to={`/bias/${news.id}`}>{news.title}</Link>
              </article>
            </section>
          </div>
      ))}
    </div>

    <div className="right-science-2">
        
        {/* <h1 className="h1">Berita Lokal</h1> */}
        {newsData.slice(0,5).map((news) => ( // Menampilkan 3 berita pertama
          <div className="right-container" key={news.id}>
              <section className="title-science">
                <img src={news.imageUrl} alt={news.title} className="img" />
                <article>
                <Link to={`/bias/${news.id}`}>{news.title}</Link>
                </article>
              </section>
            </div>
            
        ))}
      </div>
    </div>
  );
}

export default Science;