var irs = {}
if (robot_available()) {
    irs = {
        identify: function() {return 1}
    }
} else if (chrome_available()) {
    irs = {
        photo: photo,
        listen: listen,
        say: say,
        identify: function() {return 2}
    }
} else {
    irs = {
        identify: function() {return 0}
    }
}

function robot_available() {
    //check if we are running on the robot
    return false
}

function chrome_available() {
    //check all the apis are available
    return true
}

function say(phrase, callback) {
    alert(phrase)
    callback()
}
