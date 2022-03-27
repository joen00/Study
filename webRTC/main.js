const http = require("http");
const https = require("https");
const fs = require("fs");
const express = require("express");
const jwt = require("jsonwebtoken");
const app = express();

const options = {
  key: fs.readFileSync(__dirname + "/private/rootca.key"),
  cert: fs.readFileSync(__dirname + "/private/rootca.crt"),
};

const options_2 = {
  key: fs.readFileSync(__dirname + "/private/private.pem"),
  cert: fs.readFileSync(__dirname + "/private/public.pem"),
};

app.use(
  "/wrapper",
  express.static(__dirname + "/node_modules/simple-peer-wrapper/dist")
);
app.use(
  "/simple-peer",
  express.static(__dirname + "/node_modules/simple-peer")
);
app.use("/public", express.static(__dirname + "/public"));

const SECRET_KEY =
  "django-insecure-e%9jufwst@)wofot@u1kdahhxm9f!=7_$xfe=yny$n1q8sh8)m";

app.get("/main/room/video/:classroompk", (req, res) => {
  try {
    /*
        // get jwt token
        const jwt_token = req.headers['authorization'].split(' ')[1]
        jwt.verify(jwt_token, SECRET_KEY, { algorithms: ['HS256'] },(err,data)=>{
        if(err){
            throw "Not authorized"
        }
        else{
          const  guestpk = data['user_id']
          const    who = req.query['who']
          if (guestpk != who) throw "Not authorized"
        }
    })*/
    res.sendFile(__dirname + "/public/room.html");
  } catch (err) {
    console.log(err);
    res.end("error");
  }
});

http.createServer(app).listen(8080);
https.createServer(options_2, app).listen(8081);

/*
app.use("/scripts", express.static(__dirname+"/javascripts"))
app.use("/htmls", express.static(__dirname+"/htmls"))
app.use("/wrapper", express.static(__dirname+ "/node_modules/simple-peer-wrapper/dist"))
app.use('/simple-peer', express.static(__dirname + "/node_modules/simple-peer"))


app.get('/', (req,res)=>{
    res.sendFile(__dirname+'/htmls/test.html')
})

app.get('/room', (req, res)=>{
    res.sendFile(__dirname+'/htmls/room.html')
})

app.get('/:id',(req,res)=>{
    console.log(req.params)
    res.end('hi')
})
 

app.listen(3000, ()=>{
    console.log("listening")
})
*/
