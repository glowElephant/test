const express = require('express');
const cors = require('cors');
const db = require('./db');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3001;

app.get('/', (req, res) => {
  res.json({ status: 'ok' });
});

app.get('/characters', async (req, res) => {
  try {
    const { rows } = await db.query('SELECT * FROM characters ORDER BY id');
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'failed to fetch characters' });
  }
});

app.get('/characters/:id/patch_groups', async (req, res) => {
  const { id } = req.params;
  try {
    const { rows } = await db.query(
      'SELECT * FROM patch_groups WHERE character_id = $1 ORDER BY id',
      [id]
    );
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'failed to fetch patch groups' });
  }
});

app.post('/characters', async (req, res) => {
  const { name, intro } = req.body;
  try {
    const { rows } = await db.query(
      'INSERT INTO characters(name, intro) VALUES ($1,$2) RETURNING *',
      [name, intro]
    );
    res.status(201).json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'failed to create character' });
  }
});

app.get('/packages', async (req, res) => {
  try {
    const { rows } = await db.query('SELECT * FROM packages ORDER BY id');
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'failed to fetch packages' });
  }
});

app.post('/packages', async (req, res) => {
  const { character_id, name, thumbnail_url, description } = req.body;
  try {
    const { rows } = await db.query(
      'INSERT INTO packages(character_id, name, thumbnail_url, description) VALUES ($1,$2,$3,$4) RETURNING *',
      [character_id, name, thumbnail_url, description]
    );
    res.status(201).json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'failed to create package' });
  }
});

app.get('/packages/:id/items', async (req, res) => {
  const { id } = req.params;
  try {
    const { rows } = await db.query(
      'SELECT * FROM items WHERE package_id = $1 ORDER BY id',
      [id]
    );
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'failed to fetch items' });
  }
});

app.post('/items', async (req, res) => {
  const { package_id, patch_group_id, name, price, original_image_url, web_image_url } = req.body;
  try {
    const { rows } = await db.query(
      'INSERT INTO items(package_id, patch_group_id, name, price, original_image_url, web_image_url) VALUES ($1,$2,$3,$4,$5,$6) RETURNING *',
      [package_id, patch_group_id, name, price, original_image_url, web_image_url]
    );
    res.status(201).json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'failed to create item' });
  }
});

app.get('/users/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const { rows } = await db.query('SELECT * FROM users WHERE id = $1', [id]);
    if (!rows.length) return res.status(404).json({ error: 'user not found' });
    res.json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'failed to fetch user' });
  }
});

app.post('/purchase', async (req, res) => {
  const { user_id, item_id } = req.body;
  try {
    await db.query('BEGIN');
    const { rows: itemRows } = await db.query('SELECT price FROM items WHERE id = $1', [item_id]);
    if (!itemRows.length) {
      await db.query('ROLLBACK');
      return res.status(404).json({ error: 'item not found' });
    }
    const price = itemRows[0].price;
    const { rows: userRows } = await db.query('SELECT point_balance FROM users WHERE id = $1', [user_id]);
    if (!userRows.length) {
      await db.query('ROLLBACK');
      return res.status(404).json({ error: 'user not found' });
    }
    const balance = userRows[0].point_balance;
    if (balance < price) {
      await db.query('ROLLBACK');
      return res.status(400).json({ error: 'insufficient balance' });
    }
    await db.query('UPDATE users SET point_balance = point_balance - $1 WHERE id = $2', [price, user_id]);
    await db.query('INSERT INTO user_items(user_id, item_id) VALUES ($1,$2)', [user_id, item_id]);
    await db.query('COMMIT');
    res.json({ success: true });
  } catch (err) {
    await db.query('ROLLBACK');
    console.error(err);
    res.status(500).json({ error: 'failed to purchase' });
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
