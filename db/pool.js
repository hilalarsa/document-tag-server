const { Client, Pool } = require('pg');

const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

client.connect();
// const pool = new Pool({
//   user: 'postgres',
//   host: 'localhost',
//   database: 'tagger',
//   password: 'password',
//   port: 5432,
// })

module.exports = client;