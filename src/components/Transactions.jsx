import { useEffect, useState } from "react";

import PieChart from "./PieChart";

import {
    getTransactions,
    getTransactionSummary,
} from "../api";

function Transactions({ accessToken }) {
    const [payments, setPayments] = useState([]);
    const [nextCursor, setNextCursor] = useState(null);
    const [hasMore, setHasMore] = useState(false);
    const [history, setHistory] = useState([]);
    const [summary, setSummary] = useState([]);
    const [loading, setLoading] = useState(false);

    const customerId = 1;

    async function loadTransactions(cursor = null) {
        setLoading(true);

        try {
            const result = await getTransactions(
                accessToken,
                customerId,
                cursor,
                10
            );

            if (result.status !== 200) {
                return;
            }

            setPayments(
                result.data.items || []
            );

            setNextCursor(
                result.data.pagination?.next_cursor ?? null
            );

            setHasMore(
                result.data.pagination?.has_more ?? false
            );
        } finally {
            setLoading(false);
        }
    }

    async function loadSummary() {
        const result =
            await getTransactionSummary(
                accessToken,
                customerId
            );

        if (result.status !== 200) {
            return;
        }

        setSummary(
            result.data.items || []
        );
    }

    useEffect(() => {
        loadTransactions();
        loadSummary();
    }, []);

    async function handleNext() {
        if (!nextCursor || loading) {
            return;
        }

        setHistory((current) => [
            ...current,
            nextCursor,
        ]);

        await loadTransactions(
            nextCursor
        );
    }

    async function handlePrevious() {
        if (
            history.length === 0 ||
            loading
        ) {
            return;
        }

        const newHistory =
            history.slice(0, -1);

        const previousCursor =
            newHistory.length > 0
                ? newHistory[
                    newHistory.length - 1
                ]
                : null;

        setHistory(newHistory);

        await loadTransactions(
            previousCursor
        );
    }

    return (
        <div className="container">
            <h1>Payment History</h1>

            <p className="subtitle">
                Customer {customerId} payment transactions
            </p>

            <PieChart data={summary} />

            <table>
                <thead>
                    <tr>
                        <th>Transaction Id</th>
                        <th>Amount</th>
                        <th>Currency</th>
                        <th>Source</th>
                        <th>Payment Type</th>
                    </tr>
                </thead>

                <tbody>
                    {payments.map((payment) => (
                        <tr key={payment.id}>
                            <td>{payment.id}</td>

                            <td
                                className={`amount ${payment.direction}`}
                            >
                                {payment.direction ===
                                "credit"
                                    ? "+"
                                    : "-"}
                                {payment.amount}
                            </td>

                            <td>
                                {payment.currency}
                            </td>

                            <td>
                                {payment.name || "-"}
                            </td>

                            <td>
                                {payment.transaction_type}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <div className="pagination">
                <button
                    onClick={handlePrevious}
                    disabled={
                        history.length === 0 ||
                        loading
                    }
                >
                    Previous
                </button>

                <button
                    onClick={handleNext}
                    disabled={
                        !hasMore ||
                        loading
                    }
                >
                    Next
                </button>
            </div>
        </div>
    );
}

export default Transactions;