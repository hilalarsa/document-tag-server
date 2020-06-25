var express = require('express');
var router = express.Router();
var pool = require('../db/pool')

/* GET users listing. */
router.get('/', function(req, res, next) {
    pool.query('SELECT * FROM regex_isi ORDER BY id_regex_isi ASC', (error, results) => {
      if (error) {
        console.log(error)
      }
      res.status(200).json(results.rows)
      // res.render("isi", { data: results.rows });
    })
  });

router.get('/view', function(req, res, next) {
    pool.query('SELECT * FROM regex_isi ORDER BY id_regex_isi ASC', (error, results) => {
      if (error) {
        console.log(error)
      }
      // res.status(200).json(results.rows)
      res.render("isi", { data: results.rows });
    })
  });

  router.post('/', function(req, res, next) {
    let {regex_isi, keterangan} = req.body
    pool.query(`INSERT INTO regex_isi (regex_isi, keterangan) VALUES ('${regex_isi}', '${keterangan}')`, (error, results) => {
      if (error) {
        console.log(error)
      }
      // res.status(200).json(results.rows)
      res.redirect('/isi/view')
    })
  });

  router.get('/:id', function(req, res, next) {
    console.log(req.params)
    pool.query(`DELETE FROM regex_isi WHERE id_regex_isi='${req.params.id}'`, (error, results) => {
      if (error) {
        console.log(error)
      }
      // res.status(200).json(results.rows)
      res.redirect('/isi')
    })
  });

module.exports = router;
