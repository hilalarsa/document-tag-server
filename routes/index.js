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

router.post('/', upload.array('file', 10), (req, res) => {
  var file = req.files[0]
  console.log(file)
  if(file) {
    console.log("Data upload start (1/4)")
    const tempPath = file.path;
    const targetPath = path.join(__dirname, "./uploads/"+file.originalname);
    const filePath = path.join(__dirname, "./output/"+file.originalname+".txt");
    const downloadPath = path.join(__dirname, "./output_py/"+file.originalname+".txt");
    
    console.log(__dirname+"/../scripts/main.py")
    // move uploaded file to /uploads
    fs.rename(tempPath, targetPath, async(err) => {
      if (err) console.log(err)
      console.log("File uploaded in server (2/4)")
      const pythonProcess = spawn('python',[__dirname+"/../scripts/main.py", targetPath]);
      pythonProcess.stdout.on('data', (data) => {
        console.log("Spawning python process (3/4)")
        // Do something with the data returned from python script
        fs.writeFile(filePath, data.toString(), function (err) {
          if (err) console.log(err)
          console.log('File output is created successfully.(4/4)');
          // res.end()
          res.render('index',{data: filePath})
        });
      });
      // res.render('index', {data: filePath});
    })
  }else{
      res.status(400).send("Upload file failed successfully")
  }
})

router.get('/download/:id', function(req, res){
  console.log(req.params.id)
  const file = req.params.id;
  // const file = __dirname+"/output/tugas_kolektif1.jpeg.txt";
  console.log(file)
  res.download(file, function (error) {
    if(error) console.log(error)
  });
});



module.exports = router;
