import AlignmentBar from "./AlignmentBar";

function CardBeritaGrid({ data }) {
    if (!data || typeof data !== 'object') return null;

    return (
        <div className="max-w-sm bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-100">
            <a href="\news\detail">
                <img className="rounded-t-lg border-b-[2px] border-gray-200 object-cover w-full h-56" src={data.image || "/icon-news.png"} alt="Berita Image" />
                <div className="m-5">
                    <h1 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                        {data.title}
                    </h1>
                    <p className="mb-3 font-normal text-gray-700 dark:text-gray-400 truncate text-justify">
                        {data.description}
                    </p>
                    <AlignmentBar data={{ oposisi: 30, netral: 30, koalisi: 40 }} />
                </div>
            </a>
        </div>
    );
}

export default CardBeritaGrid;