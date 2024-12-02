const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const dotenv = require("dotenv");

dotenv.config();
const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Routes
const scraping = require('./routes/crawlingNewsRoutes.js');
const newsRoutes = require("./routes/newsRoutes.js");
const auth = require("./routes/authRoutes.js");
const user = require("./routes/userRoutes.js");
const admin = require("./routes/adminRoutes.js");

app.use('/scraping', scraping);
app.use("/article", newsRoutes);
app.use("/auth", auth);
app.use("/", user);
app.use("/admin", admin);


// Start Server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
