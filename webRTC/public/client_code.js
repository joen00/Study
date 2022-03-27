
const myVideo = document.getElementById("screen1");
myVideo.setAttribute("playsinline", true);
const audio_btn = document.getElementById("audio_btn");
const camera_btn = document.getElementById("camera_btn");
const cameraSelect = document.getElementById("cameras_select");


const p2Video = document.getElementById("screen2");
p2Video.setAttribute("playsinline", true);
const p3Video = document.getElementById("screen3");
p3Video.setAttribute("playsinline", true);
const p4Video = document.getElementById("screen4");
p4Video.setAttribute("playsinline", true);
const p5Video = document.getElementById("screen5");
p5Video.setAttribute("playsinline", true);
const p6Video = document.getElementById("screen6");
p6Video.setAttribute("playsinline", true);

let myStream;
let muted = false;
let cameraoff = false;
let spw;

  // usable camera list 
  async function getCameras(){
    try{
      const devices =  await navigator.mediaDevices.enumerateDevices();
      const cameras = devices.filter((device)=>device.kind==="videoinput")
  
      const currentCamera = myStream.getVideoTracks()[0];
  
      cameras.forEach(camera=>{
        const option = document.createElement("option")
        option.value = camera.deviceId
        option.innerText = camera.label
        if (currentCamera.label === camera.label) {
          option.selected = true;
        }
        cameraSelect.appendChild(option)
      })
  
    }
    catch(err){
      console.log(err);
    }
  }


// signaling server connection option
let host = 'http://localhost:9000'
path  = window.location.pathname
path = path.split('/')
const guest =  window.location.search.split("=")[1]

host += "/"+path[path.length-1]
function setup(){
  const options = {
      stream:myStream,
      serverUrl: host,
      debug:true,
      simplePeerOptions: {"private_path":path[path.length-1], "guest": guest}
  };

  // Create a new simple-peer-wrapper with a webcam stream
  spw = new SimplePeerWrapper(options);

    // Make the peer connection
    spw.connect()
    spw.on('stream',gotStream)
    spw.on('close',(data)=>{
      // socket close
    })
}


// video 설정및 요청
async function getMedia(deviceId){
  // 초기 설정
  const initialConstrains = {
    audio: false,
    video: { facingMode: "user" },
  };
  const cameraConstraints = {
    audio: false,
    video: { deviceId: { exact: deviceId } },  };

    try{
    myStream = await navigator.mediaDevices.getUserMedia(      
        deviceId ? cameraConstraints : initialConstrains);
    myVideo.srcObject = myStream;
    setup() //---> connection start
    if(!deviceId){
      await getCameras();
    }

    }
    catch(e){
      window.alert(e)
    }
   
}

getMedia()

function gotStream(value) {
  // Store incoming stream in a global variable
  partnerStream = value;  
  // set the partner video stream
  
  if (p2Video.srcObject===null){
    p2Video.srcObject = partnerStream;
    p2Video.srcObject.addEventListener("inactive",()=>{
      p2Video.srcObject=null
    })
  }
  else if(p3Video.srcObject===null) {
    p3Video.srcObject = partnerStream;
    p3Video.srcObject.addEventListener("inactive",()=>{
      p3Video.srcObject=null
    })
  }
  else if(p4Video.srcObject===null) {
    p4Video.srcObject = partnerStream;
    p4Video.srcObject.addEventListener("inactive",()=>{
      p4Video.srcObject=null
    })
  }
  else if(
    p5Video.srcObject===null) {p5Video.srcObject = partnerStream;
    p5Video.srcObject.addEventListener("inactive",()=>{
        p5Video.srcObject=null
      })
    }
  else if(p6Video.srcObject===null) {
    p6Video.srcObject = partnerStream;
    p6Video.srcObject.addEventListener("inactive",()=>{
      p6Video.srcObject=null
    })
  }else{
    window.alert("인원이 꽉찼습니다.")
    spw.close();
  }


}


window.onbeforeunload = () =>{
  spw.close();
}



// on-off handler
function handleMuteClick(){
  myStream.getAudioTracks().forEach((track) => (track.enabled = !track.enabled));

  if (muted){
    audio_btn.innerHTML = "unmute";
    muted = false;
  }
  else{
    audio_btn.innerHTML = "mute";
    muted = true;
  }
}
function handleCameraClick(){
  myStream.getVideoTracks().forEach((track) => (track.enabled = !track.enabled));
  if (cameraoff){
    camera_btn.innerHTML = "camera turn on";
    cameraoff = false;
  }
  else{
    camera_btn.innerHTML = "camera turn off";
    cameraoff = true;
  }
}

async function handleCameraChange() {
  await getMedia(cameraSelect.value);
}


audio_btn.addEventListener("click", handleMuteClick);
camera_btn.addEventListener("click", handleCameraClick);
cameraSelect.addEventListener("input", handleCameraChange);