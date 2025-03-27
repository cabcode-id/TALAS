const express = require("express");
const router = express.Router();
const newsController = require("../controllers/news.controller");

// const db = require('../services/firestore');

var admin = require("firebase-admin");
var serviceAccount = require("../config/serviceAccountKey.json");
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
});
const db = admin.firestore();

const { Firestore } = require("@google-cloud/firestore");

const firestore = new Firestore({
    projectId: "talas24",
    keyFilename: "../backend-talas/config/serviceAccountKey.json", // File credential
    databaseId: "analysisdb", // Nama database selain default
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
        const newsCollection = firestore.collection("talasnews"); // Referensi ke collection
        const snapshot = await newsCollection.get(); // Eksekusi query untuk mengambil data

        if (snapshot.empty) {
            return res.status(404).json({
                message: "No matching documents.",
                data: [],
            });
        }

        const newsList = snapshot.docs.map((doc) => ({
            id: doc.id,
            ...doc.data(),
        }));

        res.status(200).json({
            message: "Data fetched successfully",
            data: newsList,
        });
    } catch (error) {
        console.error("Error fetching documents:", error);
        res.status(500).json({
            message: "Error fetching data from Firestore",
            error: error.message,
        });
    }
});

router.post("/berita", async (req, res) => {
    try {
        const { title, content } = req.body; // Data dari request body

        // Validasi input
        if (!title || !content) {
            return res
                .status(400)
                .json({ message: "Title and content are required." });
        }

        // Tambahkan data ke koleksi `news`
        const docRef = await firestore.collection("news").add({
            title,
            content,
            createdAt: new Date().toISOString(),
        });

        // Berikan respons sukses
        res.status(201).json({
            message: "Document added successfully",
            // documentId: docRef.id,
        });
    } catch (error) {
        console.error("Error adding document:", error);
        res.status(500).json({
            message: "Error adding document to Firestore",
            error: error.message,
        });
    }
});

router.get("/sql", newsController.getAllNews);

router.get("/berita/:title", async (req, res) => {
    try {
        const title = decodeURIComponent(req.params.title);
        console.log("Decoded title:", title);
        const newsCollection = firestore.collection('talasnews');
        const snapshot = await newsCollection.where('title', '==', title).limit(1).get();
    
        if (snapshot.empty) {
        res.status(404).send("News not found");
        } else {
        const doc = snapshot.docs[0];
        res.json({ id: doc.id, ...doc.data() });
        }
    } catch (error) {
        console.error("Error fetching news detail:", error);
        res.status(500).send("Error fetching news detail");
    }
});

module.exports = router;
