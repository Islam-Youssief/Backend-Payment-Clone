import { useState } from "react";

function ForgotPassword({ onOtpSent, onBack }) {
    const [method, setMethod] = useState("email");
    const [value, setValue] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    function handleMethodChange(newMethod) {
        setMethod(newMethod);
        setValue("");
        setError("");
    }

    async function handleSubmit(e) {
        e.preventDefault();

        setError("");
        setLoading(true);

        try {
            const body = {
    email: value,
    method: method,
};

            const response = await fetch(
                "http://127.0.0.1:5000/api/auth/forgot_password",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(body),
                }
            );

            const data = await response.json();

            console.log(
                "FORGOT PASSWORD RESPONSE:",
                data
            );

            if (!response.ok) {
                setError(
                    data.message ||
                    "Could not send OTP"
                );
                return;
            }

            onOtpSent(
                method === "email"
                    ? value
                    : value
            );

        } catch (error) {
            console.error(
                "FORGOT PASSWORD ERROR:",
                error
            );

            setError(
                "Could not connect to the server"
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <h1>Forgot Password</h1>

            <p>How should we send your OTP?</p>

            <div
    style={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "center",
        alignItems: "center",
        gap: "30px",
        width: "100%",
        margin: "20px 0",
    }}
>
    <label
        style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            gap: "8px",
            cursor: "pointer",
            width: "auto",
        }}
    >
        <input
            type="radio"
            name="reset-method"
            value="email"
            checked={method === "email"}
            onChange={() => handleMethodChange("email")}
            style={{
                width: "16px",
                height: "16px",
                margin: 0,
                padding: 0,
            }}
        />

        <span>Email</span>
    </label>

    <label
        style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            gap: "8px",
            cursor: "pointer",
            width: "auto",
        }}
    >
        <input
            type="radio"
            name="reset-method"
            value="whatsapp"
            checked={method === "whatsapp"}
            onChange={() => handleMethodChange("whatsapp")}
            style={{
                width: "16px",
                height: "16px",
                margin: 0,
                padding: 0,
            }}
        />

        <span>WhatsApp</span>
    </label>
</div>

            <form onSubmit={handleSubmit}>

                <label>
    Email address
</label>

<input
    type="email"
    placeholder="Enter your email"
    value={value}
    onChange={(e) => setValue(e.target.value)}
    required
/>

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading
                        ? "Sending..."
                        : "Send OTP"}
                </button>

            </form>

            {error && (
                <p className="error">
                    {error}
                </p>
            )}

            <button
                type="button"
                onClick={onBack}
            >
                Back to Login
            </button>
        </div>
    );
}

export default ForgotPassword;