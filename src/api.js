const API_URL = "http://127.0.0.1:5000/api";

const AUTH_URL = `${API_URL}/auth`;

async function request(url, options = {}) {
    try {
        const response = await fetch(url, options);

        const text = await response.text();

        let data = {};

        if (text) {
            try {
                data = JSON.parse(text);
            } catch {
                data = {
                    message: text,
                };
            }
        }

        return {
            status: response.status,
            data,
        };
    } catch (error) {
        return {
            status: 0,
            data: {
                message:
                    error.message ||
                    "Could not connect to the server",
            },
        };
    }
}

function authHeaders(accessToken) {
    return {
        Authorization: `Bearer ${accessToken}`,
    };
}

export function register(data) {
    return request(`${AUTH_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
}

export function login(data) {
    return request(`${AUTH_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
}

export function setup2FA(challengeToken) {
    return request(`${AUTH_URL}/2fa/setup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            challenge_token: challengeToken,
        }),
    });
}

export function confirm2FA(challengeToken, code) {
    return request(`${AUTH_URL}/2fa/confirm`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            challenge_token: challengeToken,
            code,
        }),
    });
}

export function login2FA(challengeToken, code) {
    return request(`${AUTH_URL}/login/2fa`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            challenge_token: challengeToken,
            code,
        }),
    });
}

export function getPermissions(accessToken) {
    return request(`${API_URL}/permissions/`, {
        method: "GET",
        headers: {
            ...authHeaders(accessToken),
        },
    });
}

export function getImages(
    accessToken,
    cursor = null,
    limit = 20
) {
    const params = new URLSearchParams();

    params.set("limit", limit);

    if (cursor !== null) {
        params.set("cursor", cursor);
    }

    return request(
        `${API_URL}/payments/images?${params.toString()}`,
        {
            method: "GET",
            headers: {
                ...authHeaders(accessToken),
            },
        }
    );
}

export function getTransactions(
    accessToken,
    customerId,
    cursor = null,
    limit = 10
) {
    const params = new URLSearchParams();

    params.set("limit", limit);

    if (cursor !== null) {
        params.set("cursor", cursor);
    }

    return request(
        `${API_URL}/payments/transactions/customer/${customerId}?${params.toString()}`,
        {
            method: "GET",
            headers: {
                ...authHeaders(accessToken),
            },
        }
    );
}

export function getTransactionSummary(
    accessToken,
    customerId
) {
    return request(
        `${API_URL}/payments/transactions/customer/${customerId}/summary`,
        {
            method: "GET",
            headers: {
                ...authHeaders(accessToken),
            },
        }
    );
}
export function getTasks(accessToken) {
    return request(`${API_URL}/tasks/`, {
        method: "GET",
        headers: {
            ...authHeaders(accessToken)
        }
    })
}

export function createTask(
    accessToken,
    name,
    description,
    status
) {
    return request(`${API_URL}/tasks/`, {
        method: "POST",
        headers: {
            ...authHeaders(accessToken),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name,
            description,
            status
        })
    })
}

export function updateTaskStatus(
    accessToken,
    taskId,
    status
) {
    return request(
        `${API_URL}/tasks/${taskId}/status`,
        {
            method: "PATCH",
            headers: {
                ...authHeaders(accessToken),
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                status
            })
        }
    )
}

export function deleteTask(
    accessToken,
    taskId
) {
    return request(
        `${API_URL}/tasks/${taskId}`,
        {
            method: "DELETE",
            headers: {
                ...authHeaders(accessToken)
            }
        }
    )
}