const express = require('express');
const { Pool } = require('pg');
const app = express();
const port = 3000;

// Database connection
const pool = new Pool({
  user: 'your_username',
  host: 'localhost',
  database: 'codexkeep',
  password: 'your_password',
  port: 5432,
});

// Example route
app.get('/items', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM Items');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

app.listen(port, () => {
  console.log(`API is running on http://localhost:${port}`);
});
