import { useState } from "react";
import { login } from "../api";

export default function Login({
    onSetup,
    onTwoFactor,
    onForgotPassword,
}) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");

        try {
            const result = await login({
                email,
                password,
            });

            console.log("LOGIN RESPONSE:", result);

            if (result.status !== 200) {
                setError(
                    result.data?.message || "Login failed"
                );
                return;
            }

            if (result.data.requires_2fa_setup) {
                onSetup(
                    result.data.challenge_token
                );
                return;
            }

            if (result.data.requires_2fa) {
                onTwoFactor(
                    result.data.challenge_token
                );
                return;
            }

            setError(
                "Unexpected login response"
            );

        } catch (error) {
            console.error("LOGIN ERROR:", error);
            setError(
                "Could not connect to the backend"
            );
        }
    }

    return (
        <div>
            <h1>Login</h1>

            <form onSubmit={handleSubmit}>
                <input
                    placeholder="Email"
                    type="email"
                    value={email}
                    onChange={(e) =>
                        setEmail(e.target.value)
                    }
                    required
                />

                <input
                    placeholder="Password"
                    type="password"
                    value={password}
                    onChange={(e) =>
                        setPassword(e.target.value)
                    }
                    required
                />

                <button type="submit">
                    Login
                </button>
            </form>

            {error && <p>{error}</p>}

            <button
                type="button"
                onClick={onForgotPassword}
            >
                Forgot Password?
            </button>
        </div>
    );
}