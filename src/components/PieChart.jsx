import { Chart } from "chart.js/auto";
import { useEffect, useRef } from "react";

function PieChart({ data }) {
    const canvasRef = useRef(null);
    const chartData = {
        labels: data.map((item) => item.category),
        datasets: [
            {
                data: data.map((item) => item.amount)
            }
        ],
    };
      useEffect(() => {
        const chart = new Chart(canvasRef.current, {type: "pie",data: chartData
        });

        return () => {
            chart.destroy();};}, [data]);

    return <div
        className="chart-wrapper"
        style={{
          position: "z",
          width: "100%",
          height: "350px",
        }}>
            <canvas ref={canvasRef}>
                </canvas></div>;
}

export default PieChart;