export async function testShortPolling() {

    const response = await fetch(
        "http://localhost:5000/api/notifications/short-poll",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                method: "Short Polling",
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