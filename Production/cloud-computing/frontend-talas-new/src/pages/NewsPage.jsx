import CardBeritaDetail from "../components/CardNews/CardBeritaDetail";
import CardBeritaCompact from "../components/CardNews/CardBeritaCompact";

function NewsPage() {
    return (
        <div className="flex flex-row mb-20">
            <div className="w-2/3">
                <CardBeritaDetail 
                    data={{
                        time: "10 Maret 2023, 10:00 WIB",
                        title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                        description: "Maksudnya oke kalau memang Indonesia gelap. Mari kita kerja supaya Indonesia tidak gelap. Iya kan. Kok Indonesia gelap. Kabur aja deh. Kabur aja dulu deh. Habis itu Jokowi salah. Prabowo goblok. Ini tidak mengatasi,"                }}
                />
            </div>
            <div className="w-1/3">
                <div className="flex items-center justify-center border h-40 w-1/3 border-black mb-10">
                    <p>ahahah</p>
                </div>

                <hr className="my-7"/>

                <div className="grid grid-cols-1 gap-5 hover:bg-gray-100">
                    <CardBeritaCompact
                        data={{
                            title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan"
                        }}
                    />
                    <CardBeritaCompact
                        data={{
                            title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan"
                        }}
                    />
                    <CardBeritaCompact
                        data={{
                            title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan"
                        }}
                    />
                    <CardBeritaCompact
                        data={{
                            title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan"
                        }}
                    />
                </div>
            </div>
            
        </div>
    );

}

export default NewsPage;