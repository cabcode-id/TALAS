
// eslint-disable-next-line no-unused-vars
import React from "react";
import { Link } from 'react-router-dom';
import { newsData } from '../MockData';

// import './PageSwitch.css';
import './Finance.css';


// Komponen untuk menampilkan detail berita (hanya judul)
function Finance() {

  return (
    <div className="container-finance">
      {/* Kolom Kanan (opsional, bisa digunakan untuk konten lain) */}
      <div className="left-finance">
        
      <h1 className="h1">Finance</h1>
      {newsData.slice(0,5).map((news) => ( // Menampilkan 3 berita pertama
        <div className="left-container" key={news.id}>
            <section className="title-finance">
              <img src={news.imageUrl} alt={news.title} className="img" />
              <article>
              <Link to={`/bias/${news.id}`}>{news.title}</Link>
              </article>
            </section>
          </div>
      ))}
    </div>

    <div className="right-finance-2">
        
        {/* <h1 className="h1">Berita Lokal</h1> */}
        {newsData.slice(0,5).map((news) => ( // Menampilkan 3 berita pertama
          <div className="right-container" key={news.id}>
              <section className="title-finance">
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

export default Finance;