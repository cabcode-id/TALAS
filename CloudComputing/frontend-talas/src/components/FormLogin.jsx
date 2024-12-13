// eslint-disable-next-line no-unused-vars
import React, { useState } from "react";
import "./FormLogin.css"; // Import file CSS

const FormLogin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [showPassword, setShowPassword] = useState(false);

  const baseUrl = "http://localhost:5000"; // Base URL dari backend Anda

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); // Reset error message sebelum mengirim form

    // Validasi input
    if (!email || !password) {
      setError("Please fill in all fields.");
      return;
    }

    // Membuat request untuk login
    try {
      const response = await fetch(`${baseUrl}/auth/login`, {
        method: "POST", // Metode POST untuk login
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json(); // Mengambil response dari API

      if (response.ok) {
        // Jika login berhasil
        alert("You are Signed In");
        // Di sini Anda bisa menyimpan token atau melakukan redirect
      } else {
        // Jika ada error dari API
        setError(data.message || "Login failed. Please try again.");
      }
    } catch (err) {
      // Menggunakan err untuk menampilkan detail error di console
      console.error("Error occurred:", err);
      setError("An error occurred. Please try again later.");
    }
    
  };

  const toggleShowPassword = () => {
    setShowPassword(!showPassword);
  };

  // Function to validate email using regex
  const validateEmail = () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (emailRegex.test(email)) {
      alert("Email is valid");
    } else {
      alert("Email is invalid");
    }
  };

  return (
    <div className="formlogin-container">
      <div className="formlogin-wrapper">
        <h1 className="formlogin-title">LOGIN</h1>
        {error && <div className="formlogin-error">{error}</div>}
        <form className="formlogin-form" onSubmit={handleSubmit}>
          <div className="formlogin-field">
            <label htmlFor="email" className="formlogin-label">
              Email
            </label>
            <div className="formlogin-email-container">
              <input
                type="text"
                className="formlogin-input-email"
                onChange={(e) => setEmail(e.target.value)}
                value={email}
              />
              <button
                type="button"
                className="formlogin-validate-email"
                onClick={validateEmail}
              >
                Validate Email
              </button>
            </div>
          </div>

          <div className="formlogin-field">
            <label htmlFor="password" className="formlogin-label">
              Password
            </label>
            <div className="formlogin-password-container">
              <input
                type={showPassword ? "text" : "password"}
                className="formlogin-input-password"
                onChange={(e) => setPassword(e.target.value)}
                value={password}
              />
              <button
                type="button"
                className="formlogin-show-password"
                onClick={toggleShowPassword}
              >
                {showPassword ? (
                  <i className="fas fa-eye-slash fa-2x"></i>
                ) : (
                  <i className="fas fa-eye fa-2x"></i>
                )}
              </button>
            </div>
          </div>

          <button
            type="submit"
            className="formlogin-button"
          >
            Submit
          </button>
        </form>
      </div>
    </div>
  );
};

export default FormLogin;
