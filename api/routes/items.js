const express = require('express');
const router = express.Router();
const pool = require('../config/db_config');

// Get all items
router.get('/', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM Items');
        res.json(result.rows);
    } catch (err) {
        res.status(500).send(err.message);
    }
});

// Get item by ID
router.get('/:id', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM Items WHERE ItemID = $1', [req.params.id]);
        res.json(result.rows[0]);
    } catch (err) {
        res.status(500).send(err.message);
    }
});

module.exports = router;
