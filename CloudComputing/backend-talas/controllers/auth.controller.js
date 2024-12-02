// const { User } = require("../models");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const { validationResult } = require("express-validator");

const form = (req, res) => {
    return res.render("login", { errorMessages: [] });
};

const cekLogin = async (req, res) => {
    const { email, password } = req.body;

    
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        const errorMessages = errors.array().map(error => error.msg);
        return res.render("login", { errorMessages });
    }

    try {
        const user = await User.findOne({ where: { email } });
        if (!user) {
            return res.render("login", { errorMessages: ["Email atau password tidak valid"] });
        }

        const isValidPassword = await bcrypt.compare(password, user.password);
        if (!isValidPassword) {
            return res.render("login", { errorMessages: ["Email atau password tidak valid"] });
        }

        const token = jwt.sign(
            { id: user.id, email: user.email, role: user.role },
            "secretsecret",
            { expiresIn: 86400 }
        );

        res.cookie("token", token, { httpOnly: true });

        
        if (user.role == "mahasiswa") {
            return res.redirect("/");
        } else if (user.role == "dosen") {
            return res.redirect("/dosen/dashboard");
        } else if (user.role == "admin") {
            return res.redirect("/admin/dashboard");
        }

        res.status(200).send({ auth: true, token: token });
    } catch (err) {
        console.error("Error during login: ", err);
        res.status(500).json({ message: "Internal server error" });
    }
};

function logout(req, res) {
    res.clearCookie("token");
    res.redirect("/auth/login");
}

const ubahPassword = async (req, res) => {
    try {
        const { currentPassword, newPassword } = req.body;

        const user = await User.findByPk(req.userId);
        if (!user) {
            return res.status(404).json({ message: "Pengguna tidak ditemukan" });
        }

        const isPasswordValid = await bcrypt.compare(currentPassword, user.password);
        if (!isPasswordValid) {
            return res.status(401).json({ message: "Password saat ini salah" });
        }

        const hashedNewPassword = await bcrypt.hash(newPassword, 10);

        await user.update({ password: hashedNewPassword });

        return res.status(200).json({ message: "Password berhasil diubah" });
    } catch (error) {
        console.log("Error during password change:", error);
        return res.status(500).json({ message: "Terjadi kesalahan server" });
    }
};

module.exports = {
    form,
    cekLogin,
    logout,
    ubahPassword
};
