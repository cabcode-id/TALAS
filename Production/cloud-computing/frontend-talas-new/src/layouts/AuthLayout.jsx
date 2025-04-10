import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

function authLayout({ children }) {
    return (
        <div className="min-h-screen">
            <Navbar />
            <main className="flex-1 px-4 py-6">
                <Outlet /> 
            </main>
            <Footer />
        </div>
    );
}

export default authLayout;