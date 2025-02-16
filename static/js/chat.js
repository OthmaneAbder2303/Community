const socket = io.connect('http://localhost:5000'); // Fixed WebSocket connection
const username = "{{ session['username'] }}"; // Get username from session
let currentRoom = null; // Track current chat room

// Store connected users
let connectedUsers = {};

// Function to append messages to chat
function appendMessage(user, message, isSent) {
    const messageClass = isSent ? 'sent' : 'received';
    $('#messages').append(
        `<li class="message ${messageClass}"><strong>${user}:</strong> ${message}</li>`
    );
}

// Emit when sending a message
$('#send-message').click(function() {
    const message = $('#message-input').val();
    if (message && currentRoom) {
        socket.emit('message', { username: currentRoom, msg: message });
        $('#message-input').val(''); // Clear input
    }
});

// Handle incoming messages
socket.on('message', function(data) {
    appendMessage(data.username, data.msg, data.username === username);
});

// Handle user connection updates
socket.on('update_users', function(users) {
    $('#user-list').empty();
    connectedUsers = {}; // Reset user list

    users.forEach(user => {
        connectedUsers[user] = true;
        const onlineClass = 'online'; // Highlight as online
        $('#user-list').append(
            `<li class="list-group-item user-item" data-user="${user}">
                <span class="status-dot ${onlineClass}"></span> ${user}
            </li>`
        );
    });

    attachUserClickHandlers(); // Attach click events again
});

// Join a private chat room when clicking on a user
function attachUserClickHandlers() {
    $('.user-item').click(function() {
        const recipient = $(this).data('user');
        if (recipient !== username) {
            currentRoom = recipient; // Set current room

            socket.emit('join', { username: recipient });
            $('#messages').empty(); // Clear messages for new chat
            $('#chat-header').text(`Chat with ${recipient}`);
        }
    });
}

// Handle user joining
socket.emit('join', { username }); // Automatically join upon connecting

// Handle disconnect event
socket.on('disconnect', function() {
    console.log('Disconnected from server');
});

// Add friend functionality
$('#add-friend').click(function() {
    const friendName = prompt("Enter your friend's username:");
    if (friendName && friendName !== username) {
        $('#friends-list').append(
            `<li class="list-group-item">${friendName} 
                <button class="btn btn-danger btn-sm float-end remove-btn">Remove</button>
            </li>`
        );
    }
});

// Remove friend functionality
$(document).on('click', '.remove-btn', function() {
    $(this).parent().remove();
});
