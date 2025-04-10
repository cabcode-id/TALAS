import AlignmentBar from "./AlignmentBar";  
import React, { useState } from "react";


function CardBeritaDetail({ data }) {
    if (!data || typeof data !== 'object') return null;

    const [isModalOpen, setIsModalOpen] = useState(false);

    const toggleModal = () => {
        setIsModalOpen(!isModalOpen);
    };

    return (
        <div className="flex items-center text-black mx-20 w-full">
            <div className={`w-2/3 mr-10 card-berita-detail`}>
                <div className="text-start">
                    <h1 className="text-2xl font-bold">{data.title}</h1>
                    <p className="text-gray-500">{data.time}</p>

                </div>
                <img src="/icon-news.png" alt="Berita Image" className="my-5 w-full object-cover rounded-t-lg h-96 md:rounded-none md:rounded-s-lg" />

                <div className="flex flex-row gap-x-5 mt-5">
                    <AlignmentBar data={{ oposisi: 30, netral: 30, koalisi: 40 }} />
                    <button 
                        onClick={toggleModal}
                        type="button"
                        className="text-base border rounded-lg py-1 px-2 text-[#FF7C7C] border-[#FF7C7C] hover:bg-gray-400 hover:text-white">
                        Comparison
                    </button>
                </div>

                <p className="text-base font-normal mt-7 text-justify">{data.description}</p>
            </div>
            <div
                id="default-modal"
                tabIndex={-1}
                aria-hidden={isModalOpen ? "false" : "true"}  // Toggle visibility based on state
                className={`fixed inset-0 z-50 flex justify-center items-center w-full h-full ${isModalOpen ? "block" : "hidden"} bg-white/85 `} // Modal backdrop
            >
                <div className="relative p-4 w-full max-w-2xl max-h-full">
                    {/* Modal content */}
                    <div className="relative bg-white rounded-lg shadow-sm dark:bg-gray-700">
                        {/* Modal header */}
                        <div className="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600 border-gray-200">
                            <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                                Terms of Service
                            </h3>
                            <button
                                type="button"
                                onClick={toggleModal} // Close modal
                                className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
                            >
                                <svg
                                    className="w-3 h-3"
                                    aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 14 14"
                                >
                                    <path
                                        stroke="currentColor"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                                    />
                                </svg>
                                <span className="sr-only">Close modal</span>
                            </button>
                        </div>
                        {/* Modal body */}
                        <div className="p-4 md:p-5 space-y-4">
                            {/* You can add content for modal here */}
                        </div>
                        {/* Modal footer */}
                        <div className="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
                            <button
                                onClick={toggleModal} // Close modal when clicked
                                type="button"
                                className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                            >
                                I accept
                            </button>
                            <button
                                onClick={toggleModal} // Close modal when clicked
                                type="button"
                                className="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
                            >
                                Decline
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CardBeritaDetail;