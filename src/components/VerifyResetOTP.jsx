import { useState } from "react";

function VerifyResetOTP({ email, onVerified, onBack }) {
    const [otp, setOtp] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        setError("");
        setLoading(true);

        try {
            const response = await fetch(
                "http://127.0.0.1:5000/api/auth/verify_reset_otp",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        email,
                        otp,
                    }),
                }
            );

            const data = await response.json();

            console.log("VERIFY OTP RESPONSE:", data);

            if (!response.ok) {
                setError(
                    data.message || "Invalid OTP"
                );
                return;
            }

            console.log(
                "RESET TOKEN RECEIVED:",
                data.reset_token
            );

            onVerified(data.reset_token);

        } catch (error) {
            console.error(
                "VERIFY OTP ERROR:",
                error
            );

            setError(
                "Could not connect to the server"
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Verify OTP</h1>

            <p>Enter the code sent to:</p>

            <p>{email}</p>

            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="6-digit OTP"
                    value={otp}
                    onChange={(e) =>
                        setOtp(e.target.value)
                    }
                    maxLength={6}
                    required
                />

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading
                        ? "Verifying..."
                        : "Verify OTP"}
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
                Back
            </button>
        </div>
    );
}

export default VerifyResetOTP;