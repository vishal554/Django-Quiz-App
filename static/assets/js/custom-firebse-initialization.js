var firebaseConfig = {
    apiKey: "AIzaSyBB_tcFfJeuHZkDyJLGc4gT5X9h2kGAMIM",
    authDomain: "nutrify-india.firebaseapp.com",
    projectId: "nutrify-india",
    storageBucket: "nutrify-india.appspot.com",
    messagingSenderId: "238068067980",
    appId: "1:238068067980:web:906a7c37ecf90f978e55a9"
  };
    
firebase.initializeApp(firebaseConfig);
const messaging=firebase.messaging();

function IntitalizeFireBaseMessaging(url) {
    messaging
        .requestPermission()
        .then(function () {
            return messaging.getToken();
        })
        .then(function (token) {
            fetch(url+"?fcm_token="+token, {
                method: "GET",
            })
            .then((response) => {
                if (response.ok != true) {
                    console.log(response.statusText);
                    return null
                }
                else {
                    return true
                }

            })
            
        })
        .catch(function (reason) {
            console.log(reason);
        });
}

messaging.onMessage((payload) => {
    
    const notificationOption={
        body:payload.data.body,
        icon:payload.data.icon
    };

    if(Notification.permission==="granted"){
        var notification=new Notification(payload.data.title,notificationOption);

        notification.onclick=function (ev) {
            ev.preventDefault();
            update_url = payload.data.update_url
            fetch(update_url, {
                method: "GET",
            })
            .then((response) => {
                if (response.ok != true) {
                    alert(response.statusText);
                    return null
                }
            })


            window.open(payload.data.click_action,'_blank');
            notification.close();
        }
    }

});

messaging.onTokenRefresh(function () {
    messaging.getToken()
        .then(function (newtoken) {
            console.log("New Token : "+ newtoken);
        })
        .catch(function (reason) {
            console.log(reason);
        })
})
