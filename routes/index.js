var express = require('express');
var router = express.Router();

const multer = require('multer');
const upload = multer({dest: __dirname + '/uploads'});
const fs = require("fs")
const path = require("path")

const spawn = require("child_process").spawn;

// console.log(pythonProcess)

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', {data: []})
});

router.post('/', upload.single('photo'), (req, res) => {
  if(req.file) {
    const tempPath = req.file.path;
    const targetPath = path.join(__dirname, "./uploads/"+req.file.originalname);
    
    // move uploaded file to /uploads
    fs.rename(tempPath, targetPath, err => {
      if (err) console.log(err)
      // runPython(targetPath)
      const pythonProcess = spawn('python',[__dirname+"/../../scripts/main.py", targetPath]);
      // console.log(pythonProcess)
      pythonProcess.stdout.on('data', (data) => {
        // Do something with the data returned from python script
        console.log("something returned boi")
        console.log(data.toString())
        // res.redirect('/')
        res.render('index', {data: data.toString()})
      });
      // res.status(200).send(text)

    })
  }else{
      res.status(400).send("Upload file failed successfully")
  }
})



module.exports = router;
