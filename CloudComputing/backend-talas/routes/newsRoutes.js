const express = require("express");
const router = express.Router();

// Tambahkan endpoint di sini
router.get("/", (req, res) => {
    res.json({ message: "This is article" });
});
router.get("/:judul", (req, res) => {
    const judul = req.params.judul;
    res.json({ message: `${judul}` });
});

module.exports = router;
