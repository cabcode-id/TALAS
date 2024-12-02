const express = require("express");
const router = express.Router();

// Tambahkan endpoint di sini
router.get("/", (req, res) => {
    res.json({ message: "Welcome to the Home Page" });
});
module.exports = router;