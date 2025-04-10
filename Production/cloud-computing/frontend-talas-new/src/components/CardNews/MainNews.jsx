import AlignmentBar from "./AlignmentBar";  

function MainNews({ data }) {
    if (!data || typeof data !== 'object') return null;

    return (
        <div className="flex flex-col bg-white border p-5 border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
            <a className="flex flex-col items-center md:flex-row md:max-w-2xl" href="\news\detail">
                <img className="object-cover w-full rounded-t-lg h-[30rem] md:h-auto md:w-48 md:rounded-none md:rounded-s-lg" src={data.image || "/icon-news.png"} alt="Berita Image" />

                <div className="flex flex-col justify-between p-4 leading-normal">
                    <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{ data.title }</h5>
                    <p className="text-base font-normal line-clamp-6">{ data.description }</p>
                    
                </div>
            </a>
            <div>
                <AlignmentBar data={{ oposisi: 30, netral: 30, koalisi: 40 }} />
            </div>
        </div>
    );
}

export default MainNews;