document.addEventListener("DOMContentLoaded", function () {
    var socket = io.connect("http://" + document.domain + ":" + location.port);

    socket.on("message", function (data) {
        var chatBox = document.getElementById("messages");
        chatBox.innerHTML += "<p><strong>" + data.username + ":</strong> " + data.msg + "</p>";
    });

    document.getElementById("sendBtn").addEventListener("click", function () {
        var msg = document.getElementById("messageInput").value;
        socket.send({"msg": msg});
        document.getElementById("messageInput").value = "";
    });
});
