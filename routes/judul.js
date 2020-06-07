var express = require('express');
var router = express.Router();
var pool = require('../db/pool')

/* GET users listing. */
router.get('/', function(req, res, next) {
  pool.query('SELECT * FROM judul ORDER BY id_judul ASC', (error, results) => {
    if (error) {
      console.log(error)
    }
    // res.status(200).json(results.rows)
    res.render('judul', {data: results.rows})
    })
  });

module.exports = router;
