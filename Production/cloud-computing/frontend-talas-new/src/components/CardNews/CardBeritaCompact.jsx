import AlignmentBar from "./AlignmentBar";

function CardBeritaCompact({ data }) {
    if (!data || typeof data !== 'object') return null;

    return (
        <div>
            <a href="\news\detail" className="flex flex-col items-center bg-white border border-gray-200 rounded-lg shadow-sm md:flex-row md:max-w-2xl hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
                <img className="object-cover w-full rounded-t-lg h-[30rem] md:h-auto md:w-48 md:rounded-none md:rounded-s-lg" src={data.image || "/icon-news.png"} alt="Berita Image" />
                <div className="flex flex-col justify-between p-4 leading-normal">
                    <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{ data.title }</h5>
                    <AlignmentBar data={{ oposisi: 30, netral: 30, koalisi: 40 }} />
                </div>
            </a>
        </div>
    );
}

export default CardBeritaCompact;