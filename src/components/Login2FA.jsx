import { useState } from "react";
import { login2FA } from "../api";

export default function Login2FA({
    challengeToken,
    onAuthenticated,
}) {
    const [code, setCode] = useState("");
    const [error, setError] = useState("");

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");

        const result = await login2FA(
            challengeToken,
            code
        );

        if (result.status !== 200) {
            setError(result.data.message);
            return;
        }

        onAuthenticated(result.data.access_token);
    }

    return (
        <div>
            <h1>Two-Factor Authentication</h1>

            <p>Enter the code from your authenticator app.</p>

            <form onSubmit={handleSubmit}>
                <input
                    placeholder="6-digit code"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    maxLength={6}
                />

                <button type="submit">
                    Verify
                </button>
            </form>

            {error && <p>{error}</p>}
        </div>
    );
}