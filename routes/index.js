var express = require('express');
var router = express.Router();

const multer = require('multer');
const upload = multer({dest: __dirname + '/uploads'});
const fs = require("fs")
const path = require("path")

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', {title: "Hey"})
});

router.post('/', upload.single('photo'), (req, res) => {
  console.log("POST upload")
    console.log(__dirname)
    if(req.file) {
        const tempPath = req.file.path;
        const targetPath = path.join(__dirname, "./uploads/"+req.file.originalname);
        console.log(targetPath)
        fs.rename(tempPath, targetPath, err => {
          if (err) console.log(err)

          // res.status(200).send(text)
          res.redirect('/')
      })
  }else{
      res.status(400).send("Upload file failed successfully")
  }
})

module.exports = router;
