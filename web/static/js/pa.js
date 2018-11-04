var irs = (function() {
    function js_speak(phrase) {
        var msg = new SpeechSynthesisUtterance(phrase);
        window.speechSynthesis.speak(msg);
    }
    function chrome() {
        /* do some magical checking that chrome is available */
        if (typeof (window.SpeechRecognition || window.webkitSpeechRecognition) === "undefined") {
            return null;
        }

        //Voice Recognition
        function listen(words, timeout, callback) {
            var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            var recognition = new SpeechRecognition();
            
            recognition.continuous = true;
            recognition.onresult = function(event) {
                txt = event.results[event.resultIndex][0].transcript;
                console.log(txt);
                recognised = txt.split(" ");
                for (word in recognised){
                    x = words.indexOf(recognised[word]);
                    if (x!=-1){
                        if (callback){
                            callback(words.indexOf(recognised[word]));	
                        }
                        callback = null;
                    }
                }
                if (x == -1){
                    if (callback){callback(x);}					
                    callback = null;
                }
                recognition.stop();
            }
            
            recognition.start();
            setTimeout(function () {
                recognition.stop();
                if (callback){
                    callback(-1);
                    callback = null;
                }
            }, timeout);
        }
        
        //Image Capture Code
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
        
        
        
        function takePhoto(callback){
            console.log("Say cheese")
            
            var htmlCanvas = document.createElement("canvas");
            htmlCanvas.width = 1280;
            htmlCanvas.height = 720;
            htmlCanvas.style.visibility = "hidden";
            document.body.appendChild(htmlCanvas);
            imageCapture.grabFrame()
            .then(imageBitmap => {
                drawCanvas(htmlCanvas, imageBitmap);
                callback(htmlCanvas.toDataURL())
            })
            .catch(error => console.log(error));
        }

        navigator.mediaDevices.getUserMedia({video: true})
        .then(gotMedia)
        .catch(error => console.error('getUserMedia() error:', error));

        return {
            photo: takePhoto,
            listen: listen,
            say: js_speak,
            identify: function() {
                return 2;
            }
        }
    }

    function robot() {
        //check if we are running on the robot
        if(typeof irs_raw === "undefined") {
            return null;
        }
        /* setup the robot callback handlers */
        irs_raw.phraseSuccess = function(res) {
            console.log(res);
        }

        /* make the irs thingo */
        return {
            identify: function() {return 1}
        }
    }

    function basic() {
        return {
            identify: function() {
                return 0;
            },
            say: js_speak,
            listen: function(_, _, cb) {
                console.error('irs.listen is not available on this platform. use chrome');
                cb(-3);
            },
            photo: function(cb) {
                console.error('irs.photo is not available on this platform. use chrome');
                cb(null);
            }
        }
    }
    return robot() || chrome() || basic();
})()
