const jwt = require("jsonwebtoken");

function verifyTokenAndRoles(roles = []) {
    return function (req, res, next) {
        const token = req.cookies.token;

        if (!token) {
            // return res.redirect("/auth/login");
            res.json({ message: "Token not found" });
        }

        jwt.verify(token, "secretsecret", function (err, decoded) {
            if (err) {
                return res.status(500).send({
                    auth: false,
                    message: "Gagal untuk melakukan verifikasi token.",
                });
            }

            req.userId = decoded.id;
            req.userRole = decoded.role;
            req.userEmail = decoded.email;

            console.log('Token verified. User ID:', req.userId, 'Role:', req.userRole);

            if (roles.length && !roles.includes(req.userRole)) {
                if (req.userRole === "user") {
                    return res.redirect("/");
                } else if (req.userRole === "admin") {
                    return res.redirect("/admin/dashboard");
                } else {
                    return res.status(403).send({
                        auth: false,
                        message: "Anda tidak memiliki akses untuk role ini.",
                    });
                }
            }

            next();
        });
    };
}

module.exports = verifyTokenAndRoles;
