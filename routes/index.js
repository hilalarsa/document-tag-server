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
    res.render('index', {data: "Hello world"})
});

router.post('/', upload.array('file', 10), (req, res) => {
  var file = req.files[0]
  if(file) {
    console.log(req.files)
    console.log("========")
    const tempPath = file.path;
    const targetPath = path.join(__dirname, "./uploads/"+file.originalname);
    const filePath = path.join(__dirname, "./output/"+file.originalname+".txt");

    
    // move uploaded file to /uploads
    fs.rename(tempPath, targetPath, async(err) => {
      if (err) console.log(err)
      console.log("renamed")
      const pythonProcess = spawn('python',[__dirname+"/../../scripts/main.py", targetPath]);
      pythonProcess.stdout.on('data', (data) => {
        // Do something with the data returned from python script
        // messegeFromPython = JSON.stringify(data.toString('utf8')).replace("\\n", "");
        console.log(data.toString())
        fs.writeFile(filePath, data.toString(), function (err) {
          if (err) console.log(err)
          console.log('File is created successfully.');
        });
        // res.render('index', {data: messegeFromPython})
        res.redirect('/')
      });
    })
  }else{
      res.status(400).send("Upload file failed successfully")
  }
})



module.exports = router;
