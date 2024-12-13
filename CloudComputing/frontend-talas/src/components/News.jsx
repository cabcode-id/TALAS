// eslint-disable-next-line no-unused-vars
import React, { createContext, useContext, useEffect, useState } from "react";
import { Link } from "react-router-dom";

import "./News.css";
import "./Navbar.css";

const BASE_URL = import.meta.env.VITE_BASE_URL;


// Membuat context untuk berita
const NewsContext = createContext();

// Hook untuk menggunakan context
// eslint-disable-next-line react-refresh/only-export-components
export const useNews = () => useContext(NewsContext);

// Komponen utama
export default function News() {
    const [articles, setArticles] = useState([]);
    const [message, setMessage] = useState("");

    const fetchData = async () => {
        try {
            const response = await fetch(`${BASE_URL}/article`);
            const data = await response.json();
            setMessage(data.message || "");
            setArticles(data.articles || []);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <NewsContext.Provider value={{ articles, message }}>
            <div className="container">
                <NewsPage />
                <Headline />
                <BlindZone />
                <div className="news-container">
                    <News2 />
                    <News3 />
                </div>
                <div className="news-container-2">
                    {/* Tambahkan komponen lain di sini */}
                </div>
            </div>
        </NewsContext.Provider>
    );
}

function NewsPage() {
    const { articles, message } = useNews();

    if (!articles) return null;

    return (
        <div className="left">
            <h1 className="h1">{message}</h1>
            {articles.map((news) => (
                <div className="left-section" key={news.id}>
                    <div className="card">
                        <section className="article">
                            <img
                                src={news.imageUrl}
                                alt={news.title}
                                className="img"
                            />
                        </section>
                    </div>
                </div>
            ))}
        </div>
    );
}

function Headline() {
    const { articles, message } = useNews();

    if (!articles) return null;

    return (
        <div className="center-section">
            <h1 className="h1">{message}</h1>
            {articles.slice(0, 1).map((news) => (
                <div key={news.id} className="news-item">
                    <h1 className="title-headline">{news.title}</h1>
                    <img
                        src={news.imageUrl}
                        alt={news.title}
                        className="img-headline"
                    />
                </div>
            ))}
        </div>
    );
}

function BlindZone() {
    const { articles, message } = useNews();

    return (
        <div className="right-section">
            <h1 className="h1">{message}</h1>
            {articles.slice(0, 6).map((news) => (
                <div className="blind-zone" key={news.id}>
                    <section className="blind-title">
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
    const { articles, message } = useNews();

    return (
        <div className="news-container">
            <div className="left-news2">
                <h1 className="h1">{message}</h1>
                {articles.slice(0, 5).map((news) => (
                    <div className="left-container" key={news.id}>
                        <section className="title-news2">
                            <img
                                src={news.imageUrl}
                                alt={news.title}
                                className="img"
                            />
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
    const { articles, message } = useNews();

    return (
        <div className="news-container">
            <div className="right-news3">
                <h1 className="h1">{message}</h1>
                {articles.slice(0, 5).map((news) => (
                    <div className="right-container" key={news.id}>
                        <section className="title-news2">
                            <img
                                src={news.imageUrl}
                                alt={news.title}
                                className="img"
                            />
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
