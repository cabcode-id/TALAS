import AlignmentBar from "./AlignmentBar";

function TopNews({ data }) {
    if (!data || typeof data !== 'object') return null;

    return (
        <div className="flex flex-col items-center justify-center text-black">
            <a href="\news\detail">
                <h1 className="text-base font-bold">{ data.title }</h1>
                <AlignmentBar data={{ oposisi: 30, netral: 30, koalisi: 40 }} />
            </a>
        </div>
    );
}

export default TopNews;