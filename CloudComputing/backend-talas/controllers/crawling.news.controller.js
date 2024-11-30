const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

// Path folder hasil crawling
const RESULT_DIR = path.join(__dirname, '..', 'crawling_result');
if (!fs.existsSync(RESULT_DIR)) fs.mkdirSync(RESULT_DIR);

// Menjalankan file scraping
const runScraping = (req, res) => {
    const scriptName = req.query.script; // Nama file Python dari query string
    const pythonFilePath = path.join(__dirname, '..', 'crawling-news', scriptName);

    // Cek apakah file Python ada
    if (!fs.existsSync(pythonFilePath)) {
        return res.status(400).json({ error: 'Scraping script not found!' });
    }

    // Menjalankan file Python
    exec(`python ${pythonFilePath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return res.status(500).json({ error: 'Error executing script' });
        }

        if (stderr) {
            console.error(`Script stderr: ${stderr}`);
        }

        console.log(`Script stdout: ${stdout}`);
        res.status(200).json({ message: 'Scraping completed successfully!', result: stdout });
    });
};

// Menjalankan semua file scraping
const runAllScraping = (req, res) => {
    const scrapingDir = path.join(__dirname, '..', 'crawling-news');
    const scripts = fs.readdirSync(scrapingDir).filter(file => file.endsWith('.py'));

    const results = [];
    let completed = 0;

    if (scripts.length === 0) {
        return res.status(400).json({ error: 'No scraping scripts found!' });
    }

    scripts.forEach(script => {
        const scriptPath = path.join(scrapingDir, script);

        exec(`python ${scriptPath}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing ${script}: ${error.message}`);
                results.push({ script, success: false, error: error.message });
            } else {
                console.log(`Successfully executed ${script}`);
                results.push({ script, success: true });
            }

            completed++;
            if (completed === scripts.length) {
                res.status(200).json({ message: 'All scripts executed!', results });
            }
        });
    });
};

module.exports = { runScraping, runAllScraping };
