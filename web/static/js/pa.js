var irs = function() {
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
        return {
            identify: function() {return 1}
        }
    } else if (chrome_available()) {
        return {
            photo: function() {},
            listen: function() {},
            say: function(phrase, callback) {
                alert(phrase)
                callback()
            },
            identify: function() {return 2}
        }
    } else {
        return {
            identify: function() {return 0}
        }
    }
}()