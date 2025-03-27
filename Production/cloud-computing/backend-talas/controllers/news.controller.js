const db = require("./db");
exports.getAllNews = async (req, res) => {
    try {
        const [rows] = await db.query("SELECT title, content FROM news LIMIT 10;");
        res.status(200).json(rows);
    } catch (error) {
        console.error("Error fetching news:", error);
        res.status(500).json({ error: "Failed to fetch news" });
    }
};
