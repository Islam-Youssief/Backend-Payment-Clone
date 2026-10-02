import { useState, useEffect } from "react";

import {
    testShortPolling as sendShortPolling,
} from "../services/notifications/shortPolling";

import {
    testLongPolling as testLongPollingRequest,
} from "../services/notifications/longPolling";

import {
    connectSSE,
} from "../services/notifications/sse";

import {
    connectWebSocket,
} from "../services/notifications/webSocket";

import {
    testWebhook as testWebhookRequest,
} from "../services/notifications/webhook";

import {
    errorTrello,
    getErrorTrelloCount,
} from "../services/api/trello";


function NotificationLab() {

    const [logs, setLogs] = useState([]);

    const [activeMethod, setActiveMethod] =
        useState(null);

    const [status, setStatus] =
        useState("Ready");

    const [errorNotifications, setErrorNotifications] =
        useState([]);

    const [notificationCount, setNotificationCount] =
        useState(0);

    const [errorTrelloLoading, setErrorTrelloLoading] =
        useState(false);


    useEffect(() => {

        async function loadErrorCount() {

            try {

                const result =
                    await getErrorTrelloCount();

                if (result.status === 200) {

                    setNotificationCount(
                        Number(
                            result.data.notification_count
                        ) || 0
                    );
                }

            } catch (error) {

                console.error(
                    "Failed to fetch error count:",
                    error
                );
            }
        }

        loadErrorCount();

    }, []);


    async function testShortPolling() {

        const method = "Short Polling";

        setActiveMethod(method);
        setStatus("Testing...");

        const start = performance.now();

        try {

            const data =
                await sendShortPolling();

            const latency =
                performance.now() - start;

            addLog(
                method,
                data,
                latency
            );

            setStatus("Completed");

        } catch (error) {

            console.error(error);

            setStatus("Failed");
        }
    }


    async function testLongPolling() {

        const method = "Long Polling";

        setActiveMethod(method);
        setStatus("Waiting for notification...");

        try {

            const data =
                await testLongPollingRequest();

            const receivedAt =
                Date.now();

            const latency =
                receivedAt -
                data.sent_at;

            addLog(
                method,
                data,
                latency
            );

            setStatus("Completed");

        } catch (error) {

            console.error(error);

            setStatus("Failed");
        }
    }


    function testSSE() {

        const method = "SSE";

        setActiveMethod(method);
        setStatus("Connecting...");

        connectSSE({

            onOpen: () => {

                console.log(
                    "SSE connected"
                );

                setStatus("Connected");
            },


            onMessage: (data) => {

                const receivedAt =
                    Date.now();

                const latency =
                    receivedAt -
                    data.sent_at;

                console.log(
                    "SSE notification:",
                    data
                );

                console.log(
                    "Latency:",
                    latency,
                    "ms"
                );

                addLog(
                    method,
                    data,
                    latency
                );
            },


            onComplete: () => {

                console.log(
                    "SSE test completed"
                );

                setStatus("Completed");
            },


            onError: (error) => {

                console.error(
                    "SSE failed:",
                    error
                );

                setStatus("Failed");
            },

        });
    }


    function testWebSocket() {

        const method = "WebSocket";

        setActiveMethod(method);
        setStatus("Connecting...");

        connectWebSocket({

            onOpen: () => {

                console.log(
                    "WebSocket connected"
                );

                setStatus("Connected");
            },


            onMessage: (data) => {

                const receivedAt =
                    Date.now();

                const latency =
                    receivedAt -
                    data.sent_at;

                console.log(
                    "WebSocket notification:",
                    data
                );

                addLog(
                    method,
                    data,
                    latency
                );
            },


            onComplete: () => {

                console.log(
                    "WebSocket test completed"
                );

                setStatus("Completed");
            },


            onError: (error) => {

                console.error(
                    "WebSocket failed:",
                    error
                );

                setStatus("Failed");
            },

        });
    }


    async function testWebhook() {

        const method = "Webhook";

        setActiveMethod(method);
        setStatus("Sending error...");

        try {

            const data =
                await testWebhookRequest();

            addLog(
                method,
                data,
                0
            );

            setStatus("Completed");

        } catch (error) {

            console.error(error);

            setStatus("Failed");
        }
    }


    async function handleErrorTrello(errorLevel) {
    console.log("Sending:", errorLevel);

    setErrorTrelloLoading(true);
    setActiveMethod("Error Trello");
    setStatus(`Sending ${errorLevel} error...`);

    const start = performance.now();

    try {
        const result = await errorTrello(errorLevel);

        if (result.status !== 200) {
            throw new Error(
                result.data?.message ||
                "Failed to report error"
            );
        }

        const data = result.data;

        const latency = performance.now() - start;

        const notification = {
            id: Date.now(),
            method: `Error Trello - ${errorLevel}`,
            message:
                data.message ||
                data.exception ||
                "Unknown exception",
            latency,
            receivedAt: new Date(),
        };

        setErrorNotifications((previous) => [
            notification,
            ...previous,
        ]);

        if (data.notification_count !== undefined) {
            setNotificationCount(
                Number(data.notification_count)
            );
        } else {
            const countResult =
                await getErrorTrelloCount();

            if (countResult.status === 200) {
                setNotificationCount(
                    Number(
                        countResult.data.notification_count
                    ) || 0
                );
            }
        }

        setStatus(`${errorLevel} error reported`);

    } catch (error) {
        console.error("Error Trello:", error);
        setStatus("Failed");
    } finally {
        setErrorTrelloLoading(false);
    }
}

    function addLog(
        method,
        data,
        latency
    ) {

        const log = {

            id:
                data.id ||
                Date.now(),

            time:
                new Date()
                    .toLocaleTimeString(
                        "en-GB",
                        {
                            hour12: false,
                        }
                    ),

            method,

            message:
                data.message,

            latency,
        };


        setLogs(
            (previous) => [
                log,
                ...previous,
            ]
        );
    }


    function clearLogs() {

        setLogs([]);

        setErrorNotifications([]);

        setActiveMethod(null);

        setStatus("Ready");
    }


    return (

        <div className="notification-lab">

            <h1>
                Notification Transport Lab
            </h1>


            <div className="transport-grid">

                <button
                    onClick={testWebSocket}
                >
                    WebSocket
                </button>


                <button
                    onClick={testSSE}
                >
                    SSE
                </button>


                <button
                    onClick={testLongPolling}
                >
                    Long Polling
                </button>


                <button
                    onClick={testShortPolling}
                >
                    Short Polling
                </button>

            </div>


            <div className="error-actions">

                <button
                    className="send-error-button"
                    onClick={testWebhook}>
                    Send Error
                </button>
             <button onClick={() => handleErrorTrello("warning")}>
    Send Warning
</button>

<button onClick={() => handleErrorTrello("important")}>
    Send Important
</button>

<button onClick={() => handleErrorTrello("critical")}>
    Send Critical
</button>

                <button
                    className="error-trello-button"
                    onClick={handleErrorTrello}
                    disabled={
                        errorTrelloLoading
                    }
                >
                    {errorTrelloLoading
                        ? "Error Trello"
                        : "Error Trello"}
                </button>

            </div>


            <div className="notification-log">

                <div className="log-header">

                    <div className="notification-title">

                        <h2>
                            Notification Log
                        </h2>


                        {notificationCount > 0 && (

                            <span className="notification-count">

                               Sent {notificationCount} errors to Trello

                            </span>

                        )}

                    </div>


                    <button
                        onClick={clearLogs}
                    >
                        Clear
                    </button>

                </div>


                <p>

                    Method:{" "}

                    <strong>
                        {activeMethod || "None"}
                    </strong>

                </p>


                <p>

                    Status:{" "}

                    <strong>
                        {status}
                    </strong>

                </p>


                <table>

                    <thead>

                        <tr>

                            <th>
                                #
                            </th>

                            <th>
                                Time
                            </th>

                            <th>
                                Method
                            </th>

                            <th>
                                Message
                            </th>

                            <th>
                                Latency
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        {
                            logs.length === 0 &&
                            errorNotifications.length === 0
                        ? (

                            <tr>

                                <td colSpan="5">
                                    No notifications yet.
                                </td>

                            </tr>

                        ) : (

                            <>

                                {logs.map(
                                    (log, index) => (

                                        <tr
                                            key={log.id}
                                        >

                                            <td>
                                                {index + 1}
                                            </td>

                                            <td>
                                                {log.time}
                                            </td>

                                            <td>
                                                {log.method}
                                            </td>

                                            <td>
                                                {log.message}
                                            </td>

                                            <td>
                                                {Number(
                                                    log.latency
                                                ).toFixed(2)} ms
                                            </td>

                                        </tr>

                                    )
                                )}


                                {errorNotifications.map(
                                    (
                                        notification,
                                        index
                                    ) => (

                                        <tr
                                            key={
                                                notification.id
                                            }
                                            className="error-notification-row"
                                        >

                                            <td>

                                                {
                                                    logs.length +
                                                    index +
                                                    1
                                                }

                                            </td>


                                            <td>

                                                {notification.receivedAt.toLocaleTimeString(
                                                    "en-GB",
                                                    {
                                                        hour12: false,
                                                    }
                                                )}

                                            </td>


                                            <td>
                                                Error Trello
                                            </td>


                                            <td>
                                                {notification.message}
                                            </td>


                                            <td>

                                                {Number(
                                                    notification.latency
                                                ).toFixed(2)} ms

                                            </td>

                                        </tr>

                                    )
                                )}

                            </>

                        )}

                    </tbody>

                </table>

            </div>

        </div>
    );
}


export default NotificationLab;