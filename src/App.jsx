import { useState } from "react";
import Kanban_board from "./components/KanbanBoard"; 
import Register from "./components/Register";
import Setup2FA from "./components/Setup2FA";
import Login from "./components/Login";
import Login2FA from "./components/Login2FA";
import ForgotPassword from "./components/ForgotPassword";
import VerifyResetOTP from "./components/VerifyResetOTP";
import ResetPassword from "./components/ResetPassword";

import Home from "./Home";

import { getPermissions } from "./api";

import "./App.css";

function App() {
    const [screen, setScreen] = useState("register");

    const [challengeToken, setChallengeToken] =
        useState(null);

    const [accessToken, setAccessToken] =
        useState(null);

    const [permissions, setPermissions] =
        useState([]);

    const [resetEmail, setResetEmail] =
        useState(null);

    const [resetToken, setResetToken] =
        useState(null);

    async function handleAuthenticated(token) {
        setChallengeToken(null);
        setAccessToken(token);

        localStorage.setItem(
            "access_token",
            token
        );

        const result = await getPermissions(token);

        if (result.status === 200) {
            setPermissions(
                result.data.permissions || []
            );
        }
    }

    if (accessToken) {
        return (
            <Home
                accessToken={accessToken}
                permissions={permissions}
            />
        );
    }

    let content;

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

    if (screen === "login-2fa") {
        content = (
            <Login2FA
                challengeToken={challengeToken}
                onAuthenticated={handleAuthenticated}
            />
        );
    }

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
    //return <Kanban_board />;
}

export default App;