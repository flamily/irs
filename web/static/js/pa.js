var irs = (function() {
	
	//Voice Recognition
    function listen(words, timeout, callback) {
		
		var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
		var recognition = new SpeechRecognition();
		
		recognition.continuous = true;
		
		recognition.onresult = function(event) {

			txt = event.results[event.resultIndex][0].transcript
			console.log(txt);

			recognised = txt.split(" ")

			for (word in recognised){
				x = words.indexOf(recognised[word]);
				if (x!=-1){
					console.log(words.indexOf(recognised[word]));
				}			
			
			}
			
		}
		
		recognition.start();
		setTimeout(function () {recognition.stop();console.log("lalalala I can't hear you")}, 10000);

    }
	
	//Image Capture Code
	function gotMedia(mediaStream) {
	mediaStreamTrack = mediaStream.getVideoTracks()[0];
	imageCapture = new ImageCapture(mediaStreamTrack);
	console.log(imageCapture);
	
	}

	function takePhoto(callback){
		
		console.log("Say cheese")
		imageCapture.grabFrame()
	  .then(imageBitmap => {
		callback(imageBitmap);
	  })
	  .catch(error => console.log(error));
	}

	navigator.mediaDevices.getUserMedia({video: true})
	  .then(gotMedia)
	  .catch(error => console.error('getUserMedia() error:', error));
	  
	  

    function robot_available() {
        //check if we are running on the robot
        typeof irs_raw != "undefined"
    }

    function chrome_available() {
        //check all the apis are available
        return true
    }

    /* are we on the robot? */
    if (robot_available()) {
        /* setup the robot callback handlers */
        irs_raw.phraseSuccess = function(res) {
            console.log(res);
        }

        /* make the irs thingo */
        return {
            identify: function() {return 1}
        }
    } else if (chrome_available()) {
        return {
            photo: function() {},
            listen: listen,
			takePhoto: takePhoto,
            say: function(phrase) {
                var msg = new SpeechSynthesisUtterance(phrase);
                window.speechSynthesis.speak(msg);
            },
            identify: function() {
                return 2
            }
        }
    } else {
        return {
            identify: function() {return 0}
        }
    }
})()
