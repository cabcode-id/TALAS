const express = require("express");
const router = express.Router();

// Tambahkan endpoint di sini
router.get("/", (req, res) => {
    res.json({ message: "selamat datang di beranda" });
});

router.get("/account", (req, res) => {
    const judul = req.params.judul;
    res.json({ message: "ini halaman akun" });
});
router.get("/foryou", (req, res) => {
    const judul = req.params.judul;
    res.json({ message: "ini halaman untuk anda" });
});
router.get("/blindspot", (req, res) => {
    const judul = req.params.judul;
    res.json({ message: "ini halaman blindspot" });
});

module.exports = router;