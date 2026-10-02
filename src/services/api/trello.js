export async function createTrelloCard(name, desc) {
    const response = await fetch(
        "http://localhost:5000/api/trello/create_card",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: name,
                desc: desc,
            }),
        }
    );

    const data = await response.json();

    return {
        status: response.status,
        data: data,
    };
}

export async function errorTrello(errorLevel) {
    const response = await fetch(
        "http://localhost:5000/api/trello/error_trello",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                error_level: errorLevel,
            }),
        }
    );

    const data = await response.json();

    return {
        status: response.status,
        data: data,
    };
}

export async function getErrorTrelloCount() {

    const response = await fetch(
        "http://localhost:5000/api/trello/get_error_count"
    );

    const data = await response.json();

    return {
        status: response.status,
        data: data,
    };
}