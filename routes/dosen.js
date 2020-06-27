var express = require('express');
var router = express.Router();
var pool = require('../db/pool')

/* GET dosen listing. */
router.get('/', function(req, res, next) {
  pool.query('SELECT * FROM dosen ORDER BY nama_dosen ASC', (error, results) => {
    if (error) {
      console.log(error)
    }
    res.status(200).json(results.rows)
    // res.render('dosen', {data: results.rows})
  })
});

router.get('/view', function(req, res, next) {
  pool.query('SELECT * FROM dosen ORDER BY nama_dosen ASC', (error, results) => {
    if (error) {
      console.log(error)
    }
    // res.status(200).json(results.rows)
    res.render('dosen', {data: results.rows})
  })
});

router.post('/', function(req, res, next) {
  let {nama_dosen, nomor_dosen, bobot, nidn} = req.body
  pool.query(`INSERT INTO dosen (nama_dosen, nomor_dosen, nidn) VALUES ('${nama_dosen}', '${nomor_dosen}', '${nidn}')`, (error, results) => {
    if (error) {
      console.log(error)
    }
    console.log(results)
    // res.status(200).json(results.rows)
    res.redirect('/dosen/view')
  })
});

router.get('/:id', function(req, res, next) {
  console.log(req.params)
  pool.query(`DELETE FROM dosen WHERE id_dosen='${req.params.id}'`, (error, results) => {
    if (error) {
      console.log(error)
    }
    console.log(results)
    // res.status(200).json(results.rows)
    res.redirect('/dosen/view')
  })
});

module.exports = router;
