

function startTimer(duration, display, display2) {
    var timer = duration, minutes, seconds
    setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10)

        minutes = minutes < 10 ? "0" + minutes : minutes
        seconds = seconds < 10 ? "0" + seconds : seconds

        display.textContent = minutes + ":" + seconds

        display2.textContent = timer

        if (--timer < 0) {
            // submit the form
            document.getElementById('submit').click();
        }
    }, 1000)
}

window.onload = function () {
    var time_limit = document.getElementById('time_limit').value
    var time = Number(time_limit),
        display = document.querySelector('#timer_box'),
        display2 = document.querySelector('#time_remaining')
    startTimer(time, display, display2)
};

