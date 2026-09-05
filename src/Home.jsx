import { useEffect, useState } from "react";
import Gallery from "./components/Gallery";
import Transactions from "./components/Transactions";
import Kanban_board from "./components/KanbanBoard";
import { getPermissions } from "./api";
import "./index.css";

function Home() {
    const [permissions, setPermissions] = useState([]);
    const [activeTab, setActiveTab] = useState(null);
    const [loading, setLoading] = useState(true);
    const [permissionError, setPermissionError] = useState("");

    const accessToken = localStorage.getItem("access_token");
    const customerId = localStorage.getItem("customer_id");

    useEffect(() => {
        let mounted = true;

        async function loadPermissions() {
            if (!accessToken) {
                if (mounted) {
                    setPermissions([]);
                    setPermissionError("No access token found.");
                    setLoading(false);
                }
                return;
            }

            try {
                const result = await getPermissions(accessToken);

                console.log("PERMISSIONS RESULT:", result);

                if (!mounted) {
                    return;
                }

                if (result.status !== 200) {
                    setPermissions([]);
                    setPermissionError(
                        result.data?.message || "Could not load permissions."
                    );
                    setLoading(false);
                    return;
                }

                const data = result.data || {};

                const permissionList =
                    Array.isArray(data)
                        ? data
                        : Array.isArray(data.Permissions)
                            ? data.Permissions
                            : Array.isArray(data.permissions)
                                ? data.permissions
                                : Array.isArray(data.data?.Permissions)
                                    ? data.data.Permissions
                                    : Array.isArray(data.data?.permissions)
                                        ? data.data.permissions
                                        : [];

                console.log("PERMISSIONS LIST:", permissionList);

                setPermissions(permissionList);
                setPermissionError("");
                setLoading(false);
            } catch (error) {
                console.error("PERMISSIONS ERROR:", error);

                if (mounted) {
                    setPermissions([]);
                    setPermissionError("Could not load permissions.");
                    setLoading(false);
                }
            }
        }

        loadPermissions();

        return () => {
            mounted = false;
        };
    }, [accessToken]);

    const canViewTransactions =
        permissions.includes("transactions_allowed");

    const canViewGallery =
        permissions.includes("gallery_allowed");

    const canViewKanban =
        permissions.includes("kanbanBoard_allowed")

    const openTransactions = () => {
        if (!canViewTransactions) {
            return;
        }

        setActiveTab("transactions");
    };

    const openGallery = () => {
        if (!canViewGallery) {
            return;
        }

        setActiveTab("gallery");
    };

    const openKanban = () => {
        if (!canViewKanban){
            return;
        }
        
        setActiveTab("kanban");
    };

    return (
        <div className="home">
            <h1>Dashboard</h1>

            {loading ? (
                <p>Loading permissions...</p>
            ) : (
                <>
                    <p>Choose an option to continue</p>

                    {permissionError && (
                        <p>{permissionError}</p>
                    )}

                    <div className="home-buttons">
                        <button
                            type="button"
                            onClick={openTransactions}
                            disabled={!canViewTransactions}
                        >
                            Transactions
                        </button>

                        <button
                            type="button"
                            onClick={openGallery}
                            disabled={!canViewGallery}
                        >
                            Gallery
                        </button>

                        <button
                            type="button"
                            onClick={openKanban}
                        >
                            Kanban
                        </button>
                    </div>

                    {activeTab === "transactions" && canViewTransactions && (
                        <Transactions
                            accessToken={accessToken}
                            customerId={customerId}
                        />
                    )}

                    {activeTab === "gallery" && canViewGallery && (
                        <Gallery
                            accessToken={accessToken}
                        />
                    )}

                    {activeTab === "kanban" && (
                        <Kanban_board accessToken={accessToken} />
                    )}
                </>
            )}
        </div>
    );
}

export default Home;