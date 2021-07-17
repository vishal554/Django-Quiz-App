

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
            timer = 0;
            document.getElementById('submit').click();
        }
    }, 1000)
}

window.onload = function () {

    //check for Navigation Timing API support
    if (window.performance) {
        console.info("window.performance works fine on this browser");
    }
    console.info(performance.navigation.type);
    if (performance.navigation.type == performance.navigation.TYPE_RELOAD) {
        location.replace("http://127.0.0.1:8000/home/");
    } else {
        console.info( "This page is not reloaded");
    }

    var timer_amount = document.getElementById('time_limit').value;
    
    var time = Number(timer_amount),
        display = document.querySelector('#timer_box'),
        display2 = document.querySelector('#time_remaining')
    startTimer(time, display, display2)
    
};

window.addEventListener("beforeunload", function (e) {
    e.preventDefault();
    e.returnValue = ''; 
});

window.addEventListener("unload", function(e){
    e.preventDefault();
    document.getElementById('save_and_submit').click();
    for (var i=1;i<50000000; i++){}
    
});


