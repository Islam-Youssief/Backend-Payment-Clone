import { useState } from "react";

import Transactions from "./components/Transactions";
import Gallery from "./components/Gallery";
import NotificationLab from "./components/NotificationLab";
import Trello from "./components/Trello";
import KanbanBoard from "./components/KanbanBoard";
import "./index.css";
function Home({
    accessToken,
    permissions,
}) {
    const [activeTab, setActiveTab] =
        useState(null);

    const canViewTransactions =
        permissions.includes(
            "transactions_allowed"
        );

    const canViewGallery =
        permissions.includes(
            "gallery_allowed"
        );

    function goHome() {
        setActiveTab(null);
    }

    return (
        <div className="home">

            <h1>Payment Dashboard</h1>

            <div className="home-buttons">

                <button
                    disabled={!canViewTransactions}
                    onClick={() =>
                        setActiveTab("transactions")
                    }
                >
                    Transactions
                </button>

                <button
                    disabled={!canViewGallery}
                    onClick={() =>
                        setActiveTab("gallery")
                    }
                >
                    Gallery
                </button>

                <button
                    onClick={() =>
                        setActiveTab("notifications")
                    }
                >
                    Notification Lab
                </button>

                <button
                    onClick={() =>
                        setActiveTab("trello")
                    }
                >
                    Trello
                </button>

                <button
                    onClick={() =>
                        setActiveTab("kanban")
                    }
                >
                    Kanban Board
                </button>

            </div>


            {activeTab === "transactions" &&
                canViewTransactions && (
                    <div className="home-content">


                        <Transactions
                            accessToken={accessToken}
                        />

                    </div>
                )}


            {activeTab === "gallery" &&
                canViewGallery && (
                    <div className="home-content">

                     

                        <Gallery
                            accessToken={accessToken}
                        />

                    </div>
                )}


            {activeTab === "notifications" && (
                <div className="home-content">

                   
                

                    <NotificationLab
                        accessToken={accessToken}
                    />

                </div>
            )}


            {activeTab === "trello" && (
                <div className="home-content">


                    <Trello
                        accessToken={accessToken}
                    />

                </div>
            )}


            {activeTab === "kanban" && (
                <div className="home-content">


                    <KanbanBoard
                        accessToken={accessToken}
                        permissions={permissions}
                    />

                </div>
            )}

        </div>
    );
}

export default Home;