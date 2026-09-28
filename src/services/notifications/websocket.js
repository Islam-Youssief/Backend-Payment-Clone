export function connectWebSocket({
    onOpen,
    onMessage,
    onComplete,
    onError,
}) {

    const socket = new WebSocket("ws://localhost:5000/api/notifications/websocket");

    socket.onopen = () => {

        console.log(
            "WebSocket connection opened"
        );

        if (onOpen) {
            onOpen();
        }
    };


    socket.onmessage = (event) => {

        console.log(
            "WebSocket message:",
            event.data
        );

        const data =
            JSON.parse(event.data);


        if (onMessage) {
            onMessage(data);
        }
    };


    socket.onerror = (error) => {

        console.error(
            "WebSocket error:",
            error
        );

        if (onError) {
            onError(error);
        }
    };


    socket.onclose = () => {

        console.log(
            "WebSocket connection closed"
        );

        if (onComplete) {
            onComplete();
        }
    };


    return () => {
        socket.close();
    };
}