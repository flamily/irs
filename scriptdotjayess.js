console.log("Hey kids");
var htmlCanvas = document.createElement("canvas");
htmlCanvas.width = 1280;
htmlCanvas.height = 720;
document.body.appendChild(htmlCanvas);
document.getElementsByTagName('input')[0].onclick = takePic;


function gotMedia(mediaStream) {
  mediaStreamTrack = mediaStream.getVideoTracks()[0];
  imageCapture = new ImageCapture(mediaStreamTrack);
  console.log(imageCapture);
}

navigator.mediaDevices.getUserMedia({video: true})
  .then(gotMedia)
  .catch(error => console.error('getUserMedia() error:', error));
  
function drawCanvas(canvas, img) {
  canvas.width = getComputedStyle(canvas).width.split('px')[0];
  canvas.height = getComputedStyle(canvas).height.split('px')[0];
  let ratio  = Math.min(canvas.width / img.width, canvas.height / img.height);
  let x = (canvas.width - img.width * ratio) / 2;
  let y = (canvas.height - img.height * ratio) / 2;
  canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
  canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height,
      x, y, img.width * ratio, img.height * ratio);
}

function takePic(){
	imageCapture.grabFrame()
  .then(imageBitmap => {
    drawCanvas(htmlCanvas, imageBitmap);
  })
  .catch(error => ChromeSamples.log(error));
}
  
console.log("I'm a computer");