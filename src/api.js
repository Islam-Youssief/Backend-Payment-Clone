const API_URL = "http://127.0.0.1:5000/api/auth";

async function request(url, options) {
    const response = await fetch(url, options);
    const data = await response.json();

    return {
        status: response.status,
        data,
    };
}

export function register(data) {
    return request(`${API_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
}

export function login(data) {
    return request(`${API_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
}

export function setup2FA(challengeToken) {
    return request(`${API_URL}/2fa/setup`, {
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
    return request(`${API_URL}/2fa/confirm`, {
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
    return request(`${API_URL}/login/2fa`, {
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