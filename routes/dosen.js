var express = require('express');
var router = express.Router();
var pool = require('../db/pool')

/* GET dosen listing. */
router.get('/', function(req, res, next) {
  pool.query('SELECT * FROM dosen ORDER BY id_dosen ASC', (error, results) => {
    if (error) {
      console.log(error)
    }
    // res.status(200).json(results.rows)
    res.render('dosen', {data: results.rows})
  })
});

module.exports = router;
