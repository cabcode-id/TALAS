// eslint-disable-next-line no-unused-vars
import React from 'react';
import { Link } from 'react-router-dom';

import './News.css';
import './Navbar.css';

import { newsData } from '../MockData'; // Pastikan pathnya benar
// import News2 from "./News2";
export default function News() {
  return (
    <div className="container">
      <NewsPage />
      <Headline />
      <BlindZone />
      <div className='news-container'>
      <News2 />
      <News3/>
      </div>
      
      <div className='news-container-2'>
      {/* <News4 /> */}
      {/* <News5 /> */}
      </div>
      
    </div>
  );
}

// Bagian berita utama/news page sebelah kiri
function NewsPage() {
  return (
    
    <div className="left">
        
      <h1 className="h1">Berita Utama</h1>
      {newsData.slice(0, 5).map((news) => ( // Menampilkan 3 berita pertama
        <div className="left-section" key={news.id}>
          <div className="card">
            <section className="article">
              <img src={news.imageUrl} alt={news.title} className="img" />
              <article>
              <Link to={`/bias/${news.id}`}>{news.title}</Link>
              </article>
            </section>
          </div>
        </div>
      ))}
    </div>
  );
}

// Berita tengah
function Headline() {
    return (
      <div className="center-section">
        {newsData.slice(0, 1).map((news) => ( // Menampilkan 1 berita utama
          <div key={news.id} className="news-item">
            <h1 className="title-headline">
            <Link to={`/bias/${news.id}`}>{news.title}</Link>
            </h1>
            <img
              src={news.imageUrl}
              alt={news.title}
              className="img-headline"
            />
          </div>
        ))}
        <div>
              <Headline2 />

      </div>
      </div>
      
    );
  }

  function Headline2() {
    return (
      <div className="headline2">
        {newsData.slice(2, 5).map((news) => ( // Menampilkan 2 berita tambahan
          <div key={news.id} className="image-text-pair">
            {/* Gambar di kiri */}
            <img
              src={news.imageUrl}
              alt={news.title}
              className="img-center"
            />
            {/* Teks di kanan */}
            <div className="center-title">
            <Link to={`/bias/${news.id}`}>{news.title}</Link>
            </div>
          </div>
        ))}
      </div>
    );
  }
  
  
  
  

// Berita kanan / BlindZone Talas
function BlindZone() {
  
  return (
    <div className="right-section">
      <h1 className="h1">Talas Blind Zone</h1>
      {newsData.slice(4, 6).map((news) => ( // Menampilkan berita lainnya di kanan
        <div className="blind-zone" key={news.id}>
          <section className="blind-title">
              <img src={news.imageUrl} alt={news.title} className="blind-img" />
              <article>
              <Link to={`/bias/${news.id}`}>{news.title}</Link>
              </article>
            </section>
        </div>
      ))}
    </div>
  );
}

function News2() {
  return (
    <div className='news-container'>
    <div className="left-news2">
        
      <h1 className="h1">Berita Terkini</h1>
      {newsData.slice(0,5).map((news) => ( // Menampilkan 3 berita pertama
        <div className="left-container" key={news.id}>
            <section className="title-news2">
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


function News3() {
  return (
    <div className='news-container'>
    <div className="right-news3">
        
      <h1 className="h1">Berita Lokal</h1>
      {newsData.slice(0,5).map((news) => ( // Menampilkan 3 berita pertama
        <div className="right-container" key={news.id}>
            <section className="title-news2">
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