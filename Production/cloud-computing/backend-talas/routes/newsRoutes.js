const express = require("express");
const router = express.Router();
// const db = require('../services/firestore');

var admin = require("firebase-admin");
var serviceAccount = require("../config/serviceAccountKey.json");
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});
const db = admin.firestore();

const { Firestore } = require('@google-cloud/firestore');

const firestore = new Firestore({
    projectId: 'talas24',
    keyFilename: '../backend-talas/config/serviceAccountKey.json', // File credential
    databaseId: 'analysisdb', // Nama database selain default
});


// Tambahkan endpoint di sini
router.get("/", (req, res) => {
    res.json({ message: "This is article" });
});

router.get("/interest", async (req, res) => {
    res.json({ message: "This is interest" });
});



router.get("/berita", async (req, res) => {
    try {
        // Ambil koleksi dari Firestore
        const collection = firestore.collection('news');
        const snapshot = await collection.get();

        // Jika koleksi kosong
        if (snapshot.empty) {
            return res.status(404).json({
                message: 'No matching documents.',
                data: [],
            });
        }

        // Ekstrak data dari snapshot
        const berita = [];
        snapshot.forEach(doc => {
            berita.push({ id: doc.id, ...doc.data() });
        });

        // Return data dalam format JSON
        res.status(200).json({
            message: 'Data fetched successfully',
            data: berita,
        });
    } catch (error) {
        console.error('Error fetching documents:', error);
        res.status(500).json({
            message: 'Error fetching data from Firestore',
            error: error.message,
        });
    }
});

router.post("/berita", async (req, res) => {
    try {
        const { title, content } = req.body; // Data dari request body

        // Validasi input
        if (!title || !content) {
            return res.status(400).json({ message: 'Title and content are required.' });
        }

        // Tambahkan data ke koleksi `news`
        const docRef = await firestore.collection('news').add({
            title,
            content,
            createdAt: new Date().toISOString(),
        });

        // Berikan respons sukses
        res.status(201).json({
            message: 'Document added successfully',
            // documentId: docRef.id,
        });
    } catch (error) {
        console.error('Error adding document:', error);
        res.status(500).json({
            message: 'Error adding document to Firestore',
            error: error.message,
        });
    }
});

router.get("/:judul", (req, res) => {
    const judul = req.params.judul;
    res.json({ message: `${judul}` });
});

module.exports = router;
