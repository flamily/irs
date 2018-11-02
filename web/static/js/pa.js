var irs = (function() {
    function listen(words, timeout, callback) {


    }

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
