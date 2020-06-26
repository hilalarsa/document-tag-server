var express = require("express");
var router = express.Router();
var pool = require("../db/pool");

/* GET users listing. */
router.get("/", function(req, res, next) {
  pool.query(
    "SELECT * FROM regex_nomor ORDER BY id_regex_nomor ASC",
    (error, results) => {
      if (error) {
        console.log(error);
      }
      res.status(200).json(results.rows)
      // res.render("nomor", { data: results.rows });
    }
  );
});

router.get("/view", function(req, res, next) {
  pool.query(
    "SELECT * FROM regex_nomor ORDER BY id_regex_nomor ASC",
    (error, results) => {
      if (error) {
        console.log(error);
      }
      // res.status(200).json(results.rows)
      res.render("nomor", { data: results.rows });
    }
  );
});

router.post('/', function(req, res, next) {
  let {regex_nomor, keterangan} = req.body
  pool.query(`INSERT INTO regex_nomor (regex_nomor, keterangan) VALUES ('${regex_nomor}', '${keterangan}')`, (error, results) => {
    if (error) {
      console.log(error)
    }
    // res.status(200).json(results.rows)
    res.redirect('/nomor/view')
  })
});

router.get('/:id', function(req, res, next) {
  console.log(req.params)
  pool.query(`DELETE FROM regex_nomor WHERE id_regex_nomor='${req.params.id}'`, (error, results) => {
    if (error) {
      console.log(error)
    }
    // res.status(200).json(results.rows)
    res.redirect('/nomor')
  })
});

module.exports = router;
