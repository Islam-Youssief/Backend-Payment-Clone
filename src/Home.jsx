import { useState } from "react";

import Transactions from "./components/Transactions";
import Gallery from "./components/Gallery";

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

    return (
        <div className="home">
            <h1>Payment Dashboard</h1>

            <div className="home-buttons">
                <button
                    disabled={!canViewTransactions}
                    onClick={() =>
                        setActiveTab(
                            "transactions"
                        )
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
            </div>

            {activeTab === "transactions" &&
                canViewTransactions && (
                    <Transactions
                        accessToken={accessToken}
                    />
                )}

            {activeTab === "gallery" &&
                canViewGallery && (
                    <Gallery
                        accessToken={accessToken}
                    />
                )}
        </div>
    );
}

export default Home;