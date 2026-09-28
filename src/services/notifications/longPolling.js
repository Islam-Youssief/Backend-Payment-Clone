export async function testLongPolling() {

    const response = await fetch(
        "http://localhost:5000/api/notifications/long-poll",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                method: "Long Polling",
            }),
        }
    );


    if (!response.ok) {
        throw new Error(
            `HTTP ${response.status}`
        );
    }


    return response.json();
}