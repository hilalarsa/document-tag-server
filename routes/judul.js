var express = require("express");
var router = express.Router();
var pool = require("../db/pool");

/* GET users listing. */
router.get("/", function(req, res, next) {
  pool.query("SELECT * FROM judul ORDER BY id_judul ASC", (error, results) => {
    if (error) {
      console.log(error);
    }
    res.status(200).json(results.rows)
  });
});

router.get("/view", function(req, res, next) {
  pool.query("SELECT * FROM judul ORDER BY id_judul ASC", (error, results) => {
    if (error) {
      console.log(error);
    }
    res.render("judul", { data: results.rows });
  });
});

router.post('/', function(req, res, next) {
  let {tipe_judul, trigger_word} = req.body
  pool.query(`INSERT INTO judul (tipe_judul, trigger_word) VALUES ('${tipe_judul}', '${trigger_word}')`, (error, results) => {
    if (error) {
      console.log(error)
    }
    console.log(results)
    // res.status(200).json(results.rows)
    res.redirect('/judul/view')
  })
});

router.get('/:id', function(req, res, next) {
  console.log(req.params)
  pool.query(`DELETE FROM judul WHERE id_judul='${req.params.id}'`, (error, results) => {
    if (error) {
      console.log(error)
    }
    console.log(results)
    // res.status(200).json(results.rows)
    res.redirect('/judul/view')
  })
});

module.exports = router;
