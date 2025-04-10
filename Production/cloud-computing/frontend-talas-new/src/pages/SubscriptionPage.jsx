import SubscriptionCard from "../components/Subscription/SubscriptionCard";
import { Check, X } from "lucide-react";

function SubscriptionPage() {
    const headers = ["Premium", "Premium", "Premium"];

    const features = [
    { name: "Something Something", availability: [true, true, true] },
    { name: "Something Something", availability: [true, true, true] },
    { name: "Something Something", availability: [false, false, false] },
    { name: "Something Something", availability: [false, false, false] },
    ];
      
    return (
        <div className="flex flex-col items-center justify-center text-black mb-20 mt-5">

            {/* Subscription Card */}
            <div className="grid grid-cols-3 gap-20">
                <div>
                    <SubscriptionCard
                        data={{
                            priceMonth: 20000,
                            priceYear: 250000,
                            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
                        }}
                    />
                </div>
                <div>
                    <SubscriptionCard
                        data={{
                            priceMonth: 20000,
                            priceYear: 250000,
                            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
                        }}
                    />
                </div>
                <div>
                    <SubscriptionCard
                        data={{
                            priceMonth: 20000,
                            priceYear: 250000,
                            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
                        }}
                    />
                </div>
            </div>

            {/* <div className="w-full overflow-x-auto mt-10">
                <table className="min-w-full border-separate border-spacing-0 border">
                    <thead className="bg-gray-100">
                    <tr>
                        <th className="px-6 py-3 text-left font-semibold">Features</th>
                        {headers.map((title, index) => (
                        <th key={index} className="px-6 py-3 text-center font-semibold">
                            {title}
                        </th>
                        ))}
                    </tr>
                    </thead>
                    <tbody>
                    {features.map((feature, rowIndex) => (
                        <tr
                        key={rowIndex}
                        className={rowIndex >= 2 ? "bg-gray-100" : "bg-white"}
                        >
                        <td className="px-6 py-4 border-t border-gray-300">{feature.name}</td>
                        {feature.availability.map((available, colIndex) => (
                            <td
                            key={colIndex}
                            className="px-6 py-4 text-center border-t border-l border-gray-300"
                            >
                            {available ? (
                                <Check className="mx-auto w-5 h-5 text-black" />
                            ) : (
                                <X className="mx-auto w-5 h-5 text-gray-400" />
                            )}
                            </td>
                        ))}
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div> */}
        </div>
    );
}

export default SubscriptionPage;