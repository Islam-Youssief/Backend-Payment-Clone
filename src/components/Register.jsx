import { useState } from "react";
import { register } from "../api";

export default function Register({ onRegistered, onLogin }) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [phone, setPhone] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");

        const result = await register({
            username,
            email,
            phone,
            password,
        });

        if (result.status !== 201) {
            setError(result.data.message);
            return;
        }

        onRegistered(result.data.challenge_token);
    }

    return (
        <div>
            <h1>Register</h1>

            <form onSubmit={handleSubmit}>
                <input
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />

                <input
                    placeholder="Email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="tel"
                    placeholder="Phone number"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required
                />                
                <input
                    placeholder="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />

                <button type="submit">
                    Register
                </button>
            </form>

            {error && <p>{error}</p>}

            <button onClick={onLogin}>
                Already have an account?
            </button>
        </div>
    );
}