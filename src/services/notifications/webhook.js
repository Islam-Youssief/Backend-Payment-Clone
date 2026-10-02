export async function testWebhook() {

    const response = await fetch(
        "http://localhost:5000/api/notifications/webhook",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
            })
        }
    );

    if (!response.ok) {
        throw new Error(
            `HTTP ${response.status}`
        );
    }

    return response.json();
}