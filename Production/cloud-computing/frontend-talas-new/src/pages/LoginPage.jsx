import { FcGoogle } from "react-icons/fc";

function HomePage() {
    return (
      <div className="flex flex-col items-center justify-center text-black">
        <h1 className="text-2xl font-bold mt-5">Welcome, let's log in to your account</h1>
        <div className="flex flex-col justify-start mt-4 w-1/3">
            <label htmlFor="Email" className="text-xl">Email</label>
            <input type="text" className="outline-1 outline-gray-400 rounded-lg px-2 py-2" id="Email" placeholder="Enter your email" />
        </div>
        <div className="flex flex-col justify-start mt-4 w-1/3">
            <label htmlFor="Password" className="text-xl">Password</label>
            <input type="password" className="outline-1 outline-gray-400 rounded-lg px-2 py-2" id="Password" placeholder="Enter your password" />
            <p className="text-red-500">*Password must be at least 8 characters long</p>

            <div className="flex items-center justify-between">
                <div>
                    <input type="checkbox" id="remember" name="remember" value="remember" />
                    <label htmlFor="remember">Remember me</label>
                </div>
                <div>
                    <a href="#" className="text-base text-gray-500 hover:text-gray-700 hover:underline">Forgot your password?</a>
                </div>
            </div>
        </div>
        
        <button className="bg-[#FF8585] text-white w-1/3 py-3 rounded-lg mt-4 hover:bg-[#5a4141]">Login</button>
        <div className="flex flex-col w-1/3 text-center mt-1">
            <div className="flex flex-col">
                <span className="text-gray-500 text-sm">Don't have an account? <a href="/register" className="text-blue-500 hover:text-blue-700 hover:underline">Sign up</a></span>
                <a href="\register" className="bg-white text-[#FF8585] py-3 rounded-lg mt-4 hover:bg-[#5a4141] hover:text-white outline-1 outline-gray-400">Register</a>
                <div className="flex items-center text-center mt-4">
                    <hr className="flex-1 border-none h-[1px] bg-[#ccc]" />
                    <span className="mx-3 text-gray-500">Or</span>
                    <hr className="flex-1 border-none h-[1px] bg-[#ccc]" />
                </div>
                <a href="#" className="flex items-center justify-center gap-3 outline-1 py-3 rounded-lg outline-black mt-4 hover:bg-[#5a4141] hover:text-white">
                    <FcGoogle className="w-5 h-5" />
                    Continue with Google
                </a>
            </div>
        </div>
      </div>
    );
  }
  
export default HomePage;  