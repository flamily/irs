



var irs = function(){
	
	var btn = document.createElement("BUTTON");
	var t = document.createTextNode("Take Pic"); 
	btn.appendChild(t);

	var btn2 = document.createElement("BUTTON");
	var t2 = document.createTextNode("Take Pic"); 
	btn2.appendChild(t2);
	document.body.appendChild(btn);
	document.body.appendChild(btn2);

	var htmlCanvas = document.createElement("canvas");
	htmlCanvas.width = 1280;
	htmlCanvas.height = 720;
	document.body.appendChild(htmlCanvas);
	
	console.log("hi i'm an irs")
	
	commandlist = []
	
	function gotMedia(mediaStream) {
	mediaStreamTrack = mediaStream.getVideoTracks()[0];
	imageCapture = new ImageCapture(mediaStreamTrack);
	console.log(imageCapture);
	
	}
	
	
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
		console.log("hi")
		imageCapture.grabFrame()
	  .then(imageBitmap => {
		drawCanvas(htmlCanvas, imageBitmap);
	  })
	  .catch(error => console.log(error));
	}
	
	
	function listenForTen(cl){
		commandlist = cl
		recognition.start();
		setTimeout(function () {recognition.stop();console.log("lalalala I can't hear you")}, 10000);
	}
	
	
	function say(phrase){
		var msg = new SpeechSynthesisUtterance(phrase);
		window.speechSynthesis.speak(msg);	
	}
	
	console.log("Hey kids");
	var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
	var recognition = new SpeechRecognition();
	recognition.continuous = true;
	
	
	
	recognition.onresult = function(event) {

		txt = event.results[event.resultIndex][0].transcript
		console.log(txt);

		recognised = txt.split(" ")

		for (word in recognised){
			x = commandlist.indexOf(recognised[word]);
			if (x!=-1){
				console.log(commandlist.indexOf(recognised[word]));
			}			
		
		}
		
	}



	navigator.mediaDevices.getUserMedia({video: true})
	  .then(gotMedia)
	  .catch(error => console.error('getUserMedia() error:', error));
	  
	document.getElementsByTagName('button')[0].onclick = takePic;
	document.getElementsByTagName('button')[1].onclick = listenForTen(['word']);  

	console.log('im a computer')
	
}()
	
	
	








