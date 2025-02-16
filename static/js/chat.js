const socket = io.connect('http://localhost:5000/login'); // Adjust based on your app URL
const username = "{{ session['username'] }}"; // User's name from the session

let currentRoom = "general"; // Default chat room
const connectedUsers = {};

// Emit when a message is sent
$('#send-message').click(function() {
    const message = $('#message-input').val();
    if (message) {
        socket.emit('message', { msg: message });
        $('#message-input').val('');
    }
});

// Handle incoming messages
socket.on('message', function(data) {
    const messageClass = data.username === username ? 'sent' : 'received';
    $('#messages').append(
        `<li class="message ${messageClass}">${data.username}: ${data.msg}</li>`
    );
});

// Handle the list of connected users
socket.on('update_users', function(users) {
    $('#user-list').empty();
    users.forEach(user => {
        const onlineClass = connectedUsers[user] ? 'online' : 'offline';
        $('#user-list').append(
            `<li class="list-group-item"><span class="status-dot ${onlineClass}"></span>${user}</li>`
        );
    });
});

// Join the room on page load
socket.emit('join', { room: currentRoom });

// Handle adding/removing friends
$('#add-friend').click(function() {
    const friendName = prompt('Enter the friend\'s username:');
    if (friendName) {
        $('#friends-list').append(
            `<li class="list-group-item">${friendName} <button class="btn btn-danger btn-sm float-end remove-btn">Remove</button></li>`
        );
    }
});

$('#remove-friend').click(function() {
    const friendName = prompt('Enter the friend\'s username to remove:');
    if (friendName) {
        $('#friends-list li').each(function() {
            if ($(this).text().includes(friendName)) {
                $(this).remove();
            }
        });
    }
});

// Update the list of users in the sidebar when they connect/disconnect
socket.on('connect', function() {
    console.log('Socket connected');
});

socket.on('message', function(data) {
    console.log('Received message:', data);
    const messageClass = data.username === username ? 'sent' : 'received';
    $('#messages').append(
        `<li class="message ${messageClass}">${data.username}: ${data.msg}</li>`
    );
});


socket.on('disconnect', function() {
    delete connectedUsers[username];
});
