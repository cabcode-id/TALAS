const express = require("express");
const router = express.Router();

// Tambahkan endpoint di sini
router.get("/", (req, res) => {
    res.json({ message: "Welcome to Dashboard Admin" });
});
module.exports = router;
