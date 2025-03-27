const express = require("express");
const router = express.Router();
const controller = require("../controllers/auth.controller");
const verifyTokenAndRoles = require("../middleware/verifyTokenAndRole");
const beforeLogin = require("../middleware/beforeLogin.js");
const { body } = require("express-validator");


router.get("/login", beforeLogin, controller.form);
router.post("/process-login", 
    [
    body('email').isEmail().withMessage('Email tidak valid'),
    body('password').isLength({ min: 6 }).withMessage('Password harus memiliki minimal 6 karakter')
    ],
    controller.cekLogin
    );
router.get('/registrasi',beforeLogin, function(req, res, next) {
    res.render('registrasi', { title: 'Daftar' });
});
router.post('/process-regist',controller.daftar, function(req, res) {
    return res.status(200).json({ redirect: "login" });
});
router.post("/logout", controller.logout);
router.post("/changePassword", verifyTokenAndRoles(['user', 'admin']), async (req, res) => {
    try {
        await controller.ubahPassword(req, res);
    } catch (error) {
        console.log(error);
        res.status(500).json({ message: "server error" });
    }
});

module.exports = router;
