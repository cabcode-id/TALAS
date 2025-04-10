function RecentNews({ data }) {
    if (!data || typeof data !== 'object') return null;

    return (
        <div className="w-full flex justify-between mb-7 hover:bg-gray-100 p-4 rounded-md">
            <div className="flex-1 text-start w-3/4">
                <h1 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                    {data.title}
                </h1>
                <p className="mb-3 font-normal text-gray-700 dark:text-gray-400 text-justify line-clamp-2">
                    {data.description}
                </p>
                <a href="#">See more</a>
            </div>
            {data.image && (
                <img
                className="ml-5 border rounded-t-lg border-b-[2px] border-black object-cover w-52 h-40"
                src={data.image}
                alt="Berita Image"
                />
            )}

        </div>
    );
}

export default RecentNews;