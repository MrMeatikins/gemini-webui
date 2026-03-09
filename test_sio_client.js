const io = require('socket.io-client');
const socket = io('http://127.0.0.1:9999');
socket.on('connect_error', (err) => {
    console.log("ERR:", err.message, err.data);
    process.exit(0);
});
