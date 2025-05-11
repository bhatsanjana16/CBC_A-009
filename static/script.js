function sendQuery() {
    const query = document.getElementById('query').value;
    const chatBox = document.getElementById('chat-box');

    if (query.trim() !== "") {
        chatBox.innerHTML += `<div><strong>You:</strong> ${query}</div>`;
        document.getElementById('query').value = ""; // clear the input field

        // Sending the query to the backend
        fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `query=${query}`
        })
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML += `<div><strong>Assistant:</strong> ${data.response}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
        })
        .catch(error => {
            chatBox.innerHTML += `<div><strong>Error:</strong> Something went wrong!</div>`;
        });
    }
}
