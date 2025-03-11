const jwt = require('jsonwebtoken');

function beforeLogin(req, res, next) {
    const token = req.cookies.token;

    if (token) {
        jwt.verify(token, 'secretsecret', (err, decoded) => {
            if (err) {
                return res.status(401).json({
                    success: false,
                    message: "Token tidak valid atau telah kedaluwarsa.",
                });
            }

            req.userId = decoded.id;
            req.userRole = decoded.role;
            req.userEmail = decoded.email;

            if (req.userRole === "user") {
                return res.status(200).json({ redirect: "/" });
            } else if (req.userRole === "admin") {
                return res.status(200).json({ redirect: "/admin/dashboard" });
            }
        });
    } else {
        next(); // Jika tidak ada token, lanjutkan ke middleware berikutnya
    }
}

module.exports = beforeLogin;
