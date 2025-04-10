import { useLocation } from "react-router-dom";
import React from "react";
import RecentNews from "../components/CardNews/RecentNews";
 
function SearchPage() {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const query = queryParams.get("q");

    return (
        <div className="mb-20">
            <h1 className="font-bold text-3xl mb-5">Search Results for {query}</h1>
            <RecentNews 
                data={{
                    title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    image: "/icon-news.png"
                }}
            />
            <RecentNews 
                data={{
                    title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                }}
            />
            <RecentNews 
                data={{
                    title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    image: "/icon-news.png"
                }}
            />
            <RecentNews 
                data={{
                    title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                }}
            />
        </div>
    );
}

export default SearchPage;