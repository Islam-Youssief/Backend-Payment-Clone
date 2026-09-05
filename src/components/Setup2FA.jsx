import { useEffect, useState } from "react";
import { QRCodeSVG } from "qrcode.react";
import { setup2FA, confirm2FA } from "../api";

export default function Setup2FA({
    challengeToken,
    onComplete,
}) {
    const [secret, setSecret] = useState("");
    const [provisioningUri, setProvisioningUri] = useState("");
    const [code, setCode] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function setup() {
            try {
                const result = await setup2FA(
                    challengeToken
                );

                console.log(
                    "2FA SETUP RESPONSE:",
                    result
                );

                if (result.status !== 200) {
                    setError(
                        result.data?.message ||
                        "Failed to setup 2FA"
                    );
                    return;
                }

                setSecret(result.data.secret);
                setProvisioningUri(
                    result.data.provisioning_uri
                );
            } catch (error) {
                console.error(
                    "2FA SETUP ERROR:",
                    error
                );

                setError(
                    "Could not connect to the backend"
                );
            } finally {
                setLoading(false);
            }
        }

        setup();
    }, [challengeToken]);

    async function handleConfirm(event) {
        event.preventDefault();

        setError("");

        if (code.length !== 6) {
            setError(
                "The authentication code must be 6 digits"
            );
            return;
        }

        try {
            const result = await confirm2FA(
                challengeToken,
                code
            );

            console.log(
                "2FA CONFIRM RESPONSE:",
                result
            );

            if (result.status !== 200) {
                setError(
                    result.data?.message ||
                    "Invalid authentication code"
                );
                return;
            }

            onComplete();
        } catch (error) {
            console.error(
                "2FA CONFIRM ERROR:",
                error
            );

            setError(
                "Could not connect to the backend"
            );
        }
    }

    if (loading) {
        return (
            <div>
                <h1>Setup 2FA</h1>
                <p>Loading...</p>
            </div>
        );
    }

    return (
        <div>
            <h1>Setup 2FA</h1>

            <p>
                Scan this QR code with Authy or
                Google Authenticator.
            </p>

            {provisioningUri && (
                <div>
                    <QRCodeSVG
                        value={provisioningUri}
                        size={220}
                    />
                </div>
            )}


            <form onSubmit={handleConfirm}>
                <div>
                    <input
                        type="text"
                        inputMode="numeric"
                        placeholder="6-digit code"
                        value={code}
                        onChange={(e) =>
                            setCode(
                                e.target.value
                                    .replace(/\D/g, "")
                            )
                        }
                        maxLength={6}
                    />
                </div>

                <button type="submit">
                    Confirm 2FA
                </button>
            </form>

            {error && (
                <p>{error}</p>
            )}
        </div>
    );
}