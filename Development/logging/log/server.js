const express = require("express");
const cors = require("cors");
const { v4: uuidv4 } = require('uuid');
const app = express();
const mysql = require("mysql");
const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "",
  database: "news2",
});

module.exports = db;
app.use(cors());
app.use(express.json());

app.use("/login", (req, res) => {
  const { username, password } = req.body;
  
  // Check if username already exists in the database
  const checkQuery = "SELECT token FROM user WHERE username = ?";
  db.query(checkQuery, [username], (err, results) => {
    if (err) {
      console.error("Database error:", err);
      return res.status(500).json({ error: "Database error" });
    }
    
    let token;
    
    if (results.length > 0) {
      // User exists, use existing token
      token = results[0].token;
      console.log(`Existing user ${username} logged in.`);
    } else {
      // User doesn't exist, generate new token and save user
      token = uuidv4();
      const insertQuery = "INSERT INTO user (username, token) VALUES (?, ?)";
      db.query(insertQuery, [username, token], (insertErr) => {
        if (insertErr) {
          console.error("Error saving new user:", insertErr);
        } else {
          console.log(`New user ${username} created with token: ${token}`);
        }
      });
    }
    
    res.send({ token: token });
  });
});

// New logging endpoint
app.post("/log", (req, res) => {
  const { token, action } = req.body;
  
  // Insert log into database
  const query = "INSERT INTO log (token, web) VALUES (?, ?)";
  db.query(query, [token, action], (err, result) => {
    if (err) {
      console.error("Error logging action:", err);
      return res.status(500).json({ error: "Failed to log action" });
    }
    
    res.json({ success: true });
  });
});

app.listen(8080, () =>
  console.log("API is running on http://localhost:8080/login")
);
