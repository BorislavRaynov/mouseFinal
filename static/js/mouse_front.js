const ws = new WebSocket('ws://localhost:8000/ws/mouse/');

ws.onopen = function(event) {
    console.log('WebSocket connection established.');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received message:', data);
    if (data.type === 'mouse.move') {
        document.getElementById('mouse-x').textContent = 'X: ' + data.x;
        document.getElementById('mouse-y').textContent = 'Y: ' + data.y;

    } else if (data.type === 'image.capture.success') {
        document.getElementById('capture-message').textContent = data.message;
    }
};

ws.onclose = function(event) {
    console.log('WebSocket connection closed.');
};

ws.onerror = function(event) {
    console.error('WebSocket error:', event);
};