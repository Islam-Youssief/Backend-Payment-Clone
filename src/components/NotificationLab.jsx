import { useState } from "react";
import {testShortPolling as sendShortPolling,} from "../services/notifications/shortPolling";
import {testLongPolling as testLongPollingRequest,} from "../services/notifications/longPolling";
import {connectSSE as connectSSE,} from "../services/notifications/sse";
import { connectWebSocket } from "../services/notifications/webSocket";
function NotificationLab() {

    const [logs, setLogs] = useState([]);

    const [activeMethod, setActiveMethod] =useState(null);

    const [status, setStatus] =useState("Ready");

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

    const start = performance.now();


    try {

        const data =
            await testLongPollingRequest();
            const receivedAt = Date.now();


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

    function addLog(
        method,
        data,
        latency
    ) {

        const log = {
            id: data.id,

            time: new Date()
                .toLocaleTimeString(
                    "en-GB",
                    {
                        hour12: false,
                    }
                ),

            method: method,

            message: data.message,

            latency: latency,
        };


        setLogs((previous) => [
            log,
            ...previous,
        ]);
    }


    function clearLogs() {
        setLogs([]);
    }


    return (
        <div className="notification-lab">

            <h1>
                Notification Transport Lab
            </h1>


            <div className="transport-grid">

                <button onClick={testWebSocket}>
                    WebSocket
                </button>


                <button onClick={testSSE}>
                    SSE
                </button>


                <button
                    onClick={testLongPolling}
                >
                    Long Polling
                </button>


                <button
                    onClick={
                        testShortPolling
                    }
                >
                    Short Polling
                </button>

            </div>


            <div className="notification-log">

                <div className="log-header">

                    <h2>
                        Notification Log
                    </h2>


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
                            <th>#</th>
                            <th>Time</th>
                            <th>Method</th>
                            <th>Message</th>
                            <th>Latency</th>
                        </tr>

                    </thead>


                    <tbody>

                        {logs.length === 0 ? (

                            <tr>
                                <td colSpan="5">
                                    No notifications yet.
                                </td>
                            </tr>

                        ) : (

                            logs.map(
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
                                            {log.latency.toFixed(
                                                2
                                            )}{" "}
                                            ms
                                        </td>

                                    </tr>
                                )
                            )

                        )}

                    </tbody>

                </table>

            </div>

        </div>
    );
}


export default NotificationLab;