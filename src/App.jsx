import { useState } from "react";

import Register from "./components/Register";
import Setup2FA from "./components/Setup2FA";
import Login from "./components/Login";
import Login2FA from "./components/Login2FA";

import ForgotPassword from "./components/ForgotPassword";
import VerifyResetOTP from "./components/VerifyResetOTP";
import ResetPassword from "./components/ResetPassword";

import "./App.css";

function App() {
    const [screen, setScreen] = useState("register");

    const [challengeToken, setChallengeToken] =
        useState(null);

    const [accessToken, setAccessToken] =
        useState(null);

    const [resetEmail, setResetEmail] =
        useState(null);

    const [resetToken, setResetToken] =
        useState(null);

    if (accessToken) {
        return (
            <div className="app-container">
                <div className="auth-container">
                    <h1>Authenticated</h1>
                    <p>Access token received.</p>
                </div>
            </div>
        );
    }

    let content;

    /*
     * REGISTER
     */
    if (screen === "register") {
        content = (
            <Register
                onRegistered={(token) => {
                    setChallengeToken(token);
                    setScreen("setup");
                }}
                onLogin={() => {
                    setScreen("login");
                }}
            />
        );
    }

    /*
     * INITIAL 2FA SETUP
     */
    if (screen === "setup") {
        content = (
            <Setup2FA
                challengeToken={challengeToken}
                onComplete={() => {
                    setChallengeToken(null);
                    setScreen("login");
                }}
            />
        );
    }

    /*
     * LOGIN
     */
    if (screen === "login") {
        content = (
            <Login
    onSetup={(token) => {
        setChallengeToken(token);
        setScreen("setup");
    }}
    onTwoFactor={(token) => {
        setChallengeToken(token);
        setScreen("login-2fa");
    }}
    onForgotPassword={() => {
        setScreen("forgot-password");
    }}
/>
        );
    }

    /*
     * LOGIN 2FA
     */
    if (screen === "login-2fa") {
        content = (
            <Login2FA
                challengeToken={challengeToken}
                onAuthenticated={(token) => {
                    setChallengeToken(null);
                    setAccessToken(token);
                }}
            />
        );
    }

    /*
     * FORGOT PASSWORD
     */
    if (screen === "forgot-password") {
    content = (
        <ForgotPassword
            onOtpSent={(email) => {
                setResetEmail(email);
                setScreen("verify-reset-otp");
            }}
            onBack={() => {
                setScreen("login");
            }}
        />
    );
}

    /*
     * VERIFY RESET OTP
     */
    if (screen === "verify-reset-otp") {
        content = (
            <VerifyResetOTP
                email={resetEmail}
                onVerified={(token) => {
                    setResetToken(token);
                    setScreen("reset-password");
                }}
                onBack={() => {
                    setScreen("forgot-password");
                }}
            />
        );
    }

    /*
     * RESET PASSWORD
     */
    if (screen === "reset-password") {
        content = (
            <ResetPassword
                resetToken={resetToken}
                onComplete={() => {
                    setResetToken(null);
                    setResetEmail(null);
                    setScreen("login");
                }}
            />
        );
    }

    return (
        <div className="app-container">
            <div className="auth-container">
                {content}
            </div>
        </div>
    );
}

export default App;