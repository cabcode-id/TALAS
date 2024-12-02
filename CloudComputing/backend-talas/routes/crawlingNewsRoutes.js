const express = require('express');
const { runScraping, runAllScraping } = require('../controllers/crawling.news.controller');
const router = express.Router();

// Route untuk menjalankan satu file scraping
router.get('/run', runScraping);

// Route untuk menjalankan semua file scraping
router.get('/run-all', runAllScraping);

module.exports = router;
