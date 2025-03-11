const mysql = require('mysql2');

const pool = mysql.createPool({
  host: '34.101.181.121', // Ganti dengan IP Public Cloud SQL
  user: 'talasdev',                // Ganti dengan username database Anda
  password: 'talas2024*',    // Ganti dengan password database Anda
  database: 'pukulenam',       // Ganti dengan nama database Anda
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

module.exports = pool.promise();
