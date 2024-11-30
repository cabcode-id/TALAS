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
    body('password').isLength({ min: 8 }).withMessage('Password harus memiliki minimal 8 karakter')
    ],
    controller.cekLogin
    );
router.post("/logout", controller.logout);
router.post("/ubahPassword", verifyTokenAndRoles(['user', 'admin']), async (req, res) => {
    try {
        await controller.ubahPassword(req, res);
    } catch (error) {
        console.log(error);
        res.status(500).json({ message: "server error" });
    }
});

module.exports = router;
