function validate() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var data = new FormData();
    data.append("username", username);
    data.append("password", password);
    //Send the request
    fetch(host + "/api/login", {
        "method": "POST",
        "body": data
    })
        .then(res => res.json())
        .then((result) => {
            if (result.result === "failure") {
                document.getElementById("usernamelabel").value = result.desc;
            } else if (result.result === "success") {
                var token = result.token;
                var user_id = result.uid;
                username = result.user.username;
                localStorage.setItem("token", token);
                localStorage.setItem("user_id", user_id);
                localStorage.setItem("username", username);
            }
        });
}