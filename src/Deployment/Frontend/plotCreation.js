export function createPlot(data, thresholds) {
    const ctx = $('<canvas></canvas>');

    const backgroundColor = [];
    const threshold1 = thresholds[0];
    const threshold2 = thresholds[1];
    const threshold3 = thresholds[2];

    data.forEach((value) => {
        if (value < threshold1) {
            backgroundColor.push('rgba(0, 255, 0, 0.2)'); // Green
        } else if (value < threshold2) {
            backgroundColor.push('rgba(255, 165, 0, 0.2)'); // Orange
        } else if (value < threshold3) {
            backgroundColor.push('rgba(255, 0, 0, 0.2)'); // Red
        } else {
            backgroundColor.push('rgba(255, 0, 0, 0.2)'); // Red
        }
    });

    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map((_, index) => index + 1),
            datasets: [{
                label: 'Data Values',
                data: data,
                borderColor: 'rgba(0, 123, 255, 1)', // Line color
                fill: false,
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
            plugins: {
                beforeDraw: (chart) => {
                    const ctx = chart.ctx;
                    const chartArea = chart.chartArea;

                    for (let i = 0; i < data.length; i++) {
                        const x = chartArea.left + (chartArea.right - chartArea.left) * (i / (data.length - 1));
                        const y = chartArea.bottom - (chartArea.bottom - chartArea.top) * (data[i] / Math.max(...data));

                        if (data[i] < threshold1) {
                            ctx.fillStyle = 'rgba(0, 255, 0, 0.2)'; // Green
                        } else if (data[i] < threshold2) {
                            ctx.fillStyle = 'rgba(255, 165, 0, 0.2)'; // Orange
                        } else if (data[i] < threshold3) {
                            ctx.fillStyle = 'rgba(255, 0, 0, 0.2)'; // Red
                        } else {
                            ctx.fillStyle = 'rgba(255, 0, 0, 0.2)'; // Red
                        }

                        ctx.fillRect(x, chartArea.top, (chartArea.right - chartArea.left) / (data.length - 1), chartArea.bottom - chartArea.top);
                    }
                }
            }
        }
    });
}