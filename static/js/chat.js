// Simulating a simple chat environment with dynamic users and messages
document.addEventListener('DOMContentLoaded', function() {
    // Let the user input their name at the start
    let userName = prompt("Enter your name:");
    if (!userName) {
        userName = "Guest";
    }

    // Update the username in the chat header
    document.getElementById("userDisplay").innerText = `Welcome, ${userName}`;

    // Select the elements
    const messageInput = document.getElementById('messageInput');
    const sendMessageBtn = document.getElementById('sendMessageBtn');
    const chatBody = document.getElementById('chatBody');

    // Function to display the message
    function displayMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message');
        
        const avatar = document.createElement('img');
        avatar.src = sender === userName ? "https://bootdey.com/img/Content/avatar/avatar1.png" : "https://bootdey.com/img/Content/avatar/avatar3.png";
        avatar.alt = sender;

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.classList.add(sender === userName ? 'sent' : 'received');
        messageContent.innerHTML = `<p>${message}</p>`;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        chatBody.appendChild(messageDiv);

        // Auto-scroll to the bottom of the chat window
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Event listener for the send button
    sendMessageBtn.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message) {
            displayMessage(message, userName); // Display the sent message
            messageInput.value = ''; // Clear the input field
        }
    });

    // Allow pressing Enter to send a message
    messageInput.addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
            sendMessageBtn.click();
        }
    });
});
