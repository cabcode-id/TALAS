function SubscriptionCard({ data }) {
    if (!data || typeof data !== 'object') return null;

    return (
        <div className="flex flex-col items-center justify-center border border-black rounded-md h-auto w-80 p-8 shadow-sm">
            <div className="text-black flex flex-col items-center justify-center">
                <h2 className="border bg-[#FFD7CF] text-2xl rounded-lg w-36 text-center py-2 border-none font-normal">Premium</h2>
                <p className="text-justify mt-3 mb-7">Suitable for entry user who wants to get more news.</p>

            </div>
            
            <div className="w-full flex flex-col items-center justify-center">
                <p className="text-black font-semibold text-2xl">Rp { data.priceMonth } <span className="text-base text-[#8C8C8C] font-normal">/Month*</span></p>
                <p className="text-base text-[#8C8C8C]">Billed as Rp { data.priceYear }/Year*</p>
                <p className="my-3 text-[#EB6969] text-xl font-semibold">+ 2 Month's Free</p>
                <hr className="mt-3 mb-6 w-full"/>
                <p className="text-justify"> { data.description } </p>
            </div>


            <a href="#" className="text-base border rounded-lg text-white bg-[#FF7C7C] w-full py-3 text-center mt-16 hover:bg-gray-400 hover:text-black">Subscribe</a>
        </div>
    );
}

export default SubscriptionCard;