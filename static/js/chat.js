document.addEventListener("DOMContentLoaded", function () {
    const socket = io.connect("http://localhost:5000");
    const username = "{{ session['username'] }}";

    // Fetch previous messages
    fetch(`/get_messages`)
        .then(response => response.json())
        .then(messages => {
            const messagesList = document.getElementById("messages");
            messages.forEach(msg => {
                const li = document.createElement("li");
                li.innerHTML = `<b>${msg.sender}:</b> ${msg.message} <span class='timestamp'>(${msg.timestamp})</span>`;
                messagesList.appendChild(li);
            });
        });

    // Update user list
    socket.on("update_users", function(users) {
        const userList = document.getElementById("user-list");
        userList.innerHTML = "";
        users.forEach(user => {
            const li = document.createElement("li");
            li.textContent = user;
            userList.appendChild(li);
        });
    });

    // Send message
    document.getElementById("send-message").addEventListener("click", function () {
        const messageInput = document.getElementById("message-input");
        const message = messageInput.value;
        if (message) {
            socket.emit("message", { msg: message });
            messageInput.value = "";
        }
    });

    // Receive message
    socket.on("message", function(data) {
        const messagesList = document.getElementById("messages");
        const li = document.createElement("li");
        li.innerHTML = `<b>${data.username}:</b> ${data.msg} <span class='timestamp'>(${data.timestamp})</span>`;
        messagesList.appendChild(li);
    });

    // Logout button
    document.getElementById("logout").addEventListener("click", function () {
        window.location.href = "/logout";
    });
});
