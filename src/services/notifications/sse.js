export function connectSSE({
    onMessage,
    onOpen,
    onComplete,
    onError,
}) {

    const eventSource = new EventSource(
        "http://localhost:5000/api/notifications/sse"
    );


    eventSource.onopen = () => {

        console.log(
            "SSE connection opened"
        );

        if (onOpen) {
            onOpen();
        }
    };


    eventSource.addEventListener(
        "notification",
        (event) => {

            console.log(
                "SSE notification event:",
                event.data
            );


            const data =
                JSON.parse(event.data);


            if (onMessage) {
                onMessage(data);
            }
        }
    );


    eventSource.addEventListener(
        "complete",
        () => {

            console.log(
                "SSE test completed"
            );

            eventSource.close();


            if (onComplete) {
                onComplete();
            }
        }
    );


    eventSource.onerror = (error) => {

        console.error(
            "SSE error:",
            error
        );

        if (
            eventSource.readyState !==
            EventSource.CLOSED
        ) {

            if (onError) {
                onError(error);
            }
        }
    };


    return () => {
        eventSource.close();
    };
}