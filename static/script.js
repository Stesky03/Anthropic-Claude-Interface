let id = Date.now();

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('messageForm');
    const chatBox = document.getElementById('chatBox');
    const messageInput = document.getElementById('messageInput');

    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.innerHTML = message;
        chatBox.appendChild(messageElement);
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = document.getElementById('messageInput').value;
        addMessage(message, 'client');
        
        const mode = document.getElementById('prompt-select').value;
        if (!message) return;
        document.getElementById('messageInput').value="";
        
        try {
            const response = await fetch('/send-message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: id, msg: message, mode: mode}),
            });

            if (response.ok) {
                const data = await response.text();
                dataMD = marked.parse(data);
                addMessage(dataMD, 'server');
            } else {
                throw new Error('Failed to send message');
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('Server Error', 'server');
        }
    });
});
