const jwt = require ('jsonwebtoken')

function beforeLogin(req, res, next) {
const token = req.cookies.token;

if (token) {
jwt.verify(token,'secretsecret', function (err, decoded) {
    if (err) {
    return res
        .status(500)
        .send({
        auth: false,
        message: "Gagal untuk melakukan verifikasi token.",
        });
    }

    req.userId = decoded.id;
    req.userRole = decoded.role;
    req.userEmail = decoded.email;
});
if (req.userRole == "user") {
    return res.redirect("/");
} else if (req.userRole == "admin") {
    return res.redirect("/admin/dashboard");
}
}

next();
}

module.exports = beforeLogin;
