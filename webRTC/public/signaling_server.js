const SimplePeerServer = require('simple-peer-server');


const http = require('http');
const https = require('https');
const path = require('path')
const app = require('express')()
const fs = require('fs');


base_dir = path.join(__dirname, '../')
const options = { 
    key: fs.readFileSync(base_dir+"/private/rootca.key"), 
    cert: fs.readFileSync(base_dir+"/private/rootca.crt") 
}

const options_2 = { 
    key: fs.readFileSync(base_dir+"/private/private.pem"), 
    cert: fs.readFileSync(base_dir+"/private/public.pem") 
}

const server = http.createServer(app);
const server_s = https.createServer(options_2);
const spServer = new SimplePeerServer(server, false);
const spServer_s = new SimplePeerServer(server_s, true);




server.listen(9000 ,()=>{
    console.log("signaling server listening")
});

server_s.listen(9443,()=>{
    console.log("https signaling server listening")
});
