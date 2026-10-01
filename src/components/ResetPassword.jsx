import { useState } from "react";

function ResetPassword({ resetToken, onComplete }) {
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        setError("");
        setMessage("");

        if (newPassword !== confirmPassword) {
            setError("Passwords don't match");
            return;
        }

        console.log(
            "RESET TOKEN BEING SENT:",
            resetToken
        );

        setLoading(true);

        try {
            const response = await fetch(
                "http://127.0.0.1:5000/api/auth/reset_password",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        reset_token: resetToken,
                        new_password: newPassword,
                        confirm_new_password:
                            confirmPassword,
                    }),
                }
            );

            const data = await response.json();

            console.log(
                "RESET PASSWORD RESPONSE:",
                data
            );

            if (!response.ok) {
                setError(
                    data.message ||
                    "Password reset failed"
                );
                return;
            }

            setMessage(data.message);

            setTimeout(() => {
                onComplete();
            }, 1000);

        } catch (error) {
            console.error(
                "RESET PASSWORD ERROR:",
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
            <h1>Reset Password</h1>

            <form onSubmit={handleSubmit}>
                <input
                    type="password"
                    placeholder="New password"
                    value={newPassword}
                    onChange={(e) =>
                        setNewPassword(e.target.value)
                    }
                    required
                />

                <input
                    type="password"
                    placeholder="Confirm new password"
                    value={confirmPassword}
                    onChange={(e) =>
                        setConfirmPassword(e.target.value)
                    }
                    required
                />

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading
                        ? "Resetting..."
                        : "Reset Password"}
                </button>
            </form>

            {error && (
                <p className="error">
                    {error}
                </p>
            )}

            {message && (
                <p>{message}</p>
            )}
        </div>
    );
}

export default ResetPassword;