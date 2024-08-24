document.addEventListener('DOMContentLoaded', function () {
    const startMatchButton = document.getElementById('start-match-button');
    const form = document.getElementById('question-form');
    const statusText = document.getElementById('status-text');

    if (startMatchButton) {
        startMatchButton.addEventListener('click', function () {
            console.log("Button has been clicked!")
            // Show "Waiting for player..." text immediately after clicking "Start Match"
            if (!statusText) {
                statusText = document.createElement('p');
                statusText.id = 'status-text';
                document.body.appendChild(statusText);
            }
            statusText.textContent = 'Waiting for player...';

            fetch('/start-match/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const roomId = data.room_id;

                    const checkRoomStatus = setInterval(() => {
                        fetch('/check-room-status/', {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken'),
                                'Content-Type': 'application/json'
                            }
                        })
                        .then(response => response.json())
                        .then(statusData => {
                            if (statusData.status === 'ready') {
                                clearInterval(checkRoomStatus);
                                statusText.textContent = 'Match Found!';
                                setTimeout(() => {
                                    window.location.href = statusData.redirect_url;
                                }, 2000); // Wait for 2 seconds before redirecting
                            }
                        });
                    }, 5000); // Check every 5 seconds
                }
            });
        });
    }
    
    if (form) {
        form.addEventListener('submit', function (event) {
            console.log("This is 2nd match")
            event.preventDefault();  // Prevent default form submission

            const formData = new FormData(form);
            formData.append('room_id', getRoomId());  // Add room_id to form data

            fetch('/submit-answer/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                statusText.textContent = data.message;
                if (data.status === 'success') {
                    // Redirect or perform other actions on success
                    setTimeout(() => {
                        window.location.href = '/home/'; // Redirect to home or other page
                    }, 2000); // Wait for 2 seconds before redirecting
                }
            });
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function getRoomId() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('room_id');
    }
});
