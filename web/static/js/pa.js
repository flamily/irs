var irs = (function() {
    function chrome() {
        function chrome_available() {
            //check all the apis are available
            return true
        }
        function listen(words, timeout, callback) {

        }
        if (!chrome_available()) {
            return null
        }
        return {
            photo: function() {},
            listen: listen,
            say: function(phrase) {
                var msg = new SpeechSynthesisUtterance(phrase);
                window.speechSynthesis.speak(msg);
            },
            identify: function() {
                return 2
            }
        }
    }

    function robot() {
        //check if we are running on the robot
        if(typeof irs_raw === "undefined") {
            return null
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
    return robot() || chrome() || {identify: function() {return 0}}
})()
