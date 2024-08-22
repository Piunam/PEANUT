document.addEventListener('DOMContentLoaded', function () {
    const startMatchButton = document.getElementById('start-match-button');

    startMatchButton.addEventListener('click', function () {
        // Show "Waiting for player..." text immediately after clicking "Start Match"
        let statusText = document.getElementById('status-text');
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
                            document.getElementById('status-text').textContent = 'Match Found!';
                            console.log(statusData)
                            setTimeout(() => {
                                window.location.href = statusData.redirect_url;
                            }, 2000); // Wait for 2 seconds before redirecting
                        }
                    });
                }, 5000); // Check every 5 seconds
            }
        });
    });
});

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
