require('dotenv').config(); // Load environment variables
const express = require('express');
const path = require('path');
const { Pool } = require('pg');

const app = express();
const port = 3000;

// PostgreSQL connection setup
const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
});

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, '../frontend/public')));

// Route to fetch all items from the database
app.get('/items', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM Items'); // Adjust table name if needed
    res.json(result.rows);
  } catch (err) {
    console.error('[ERROR] Failed to fetch items:', err);
    res.status(500).send('Failed to fetch items.');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
