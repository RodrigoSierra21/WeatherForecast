
function createPlot(data, thresholds, column) {
    const ctx = $('<canvas id="canvas"></canvas>');
    $('#' + column + 'div').append(ctx);

    const threshold1 = thresholds[0];
    const threshold2 = thresholds[1];
    const threshold3 = thresholds[2];

    // Create an array to store colors based on the thresholds
    const colors = data.map(value => {
        if (value < threshold1) {
            return 'rgba(0, 255, 0, 1)'; // Green
        } else if (value < threshold2) {
            return 'rgba(255, 165, 0, 1)'; // Orange
        } else if (value < threshold3) {
            return 'rgba(255, 0, 0, 1)'; // Red
        } else {
            return 'rgba(255, 0, 0, 1)'; // Red (or you can choose a different color for extreme cases)
        }
    });

    // Create an array for line colors based on the segments
    const lineColors = [];
    for (let i = 0; i < data.length - 1; i++) {
        lineColors.push(colors[i + 1]); // The color of the line segment is the color of the end point
    }
    lineColors.push(colors[colors.length - 1]);

    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map((_, index) => index + 1), // Assuming labels are just index numbers
            datasets: [{
                label: 'Data Values',
                data: data,
                borderColor: lineColors, // Set line colors based on the segments
                fill: false,
                borderWidth: 2,
                pointBackgroundColor: colors, // Set point colors based on thresholds
                pointBorderColor: colors, // Optional: set border color to match
                pointRadius: 5, // Size of the points
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

                    // Drawing rectangles with corresponding background colors for visual reference
                    for (let i = 0; i < data.length; i++) {
                        const x = chartArea.left + (chartArea.right - chartArea.left) * (i / (data.length - 1));
                        const y = chartArea.bottom - (chartArea.bottom - chartArea.top) * (data[i] / Math.max(...data));

                        ctx.fillStyle = colors[i]; // Use the colors mapped to each value

                        // Draw rectangle for each value
                        ctx.fillRect(x - 5, chartArea.top, 10, chartArea.bottom - chartArea.top); // Adjust as needed
                    }
                }
            }
        }
    });
}


// Create O3div
var O3div = $('<div id = "O3div" ></div>');
const O3thresholds = [100,200,200];
var O3Title = $('<div id = "O3title" ></div>');
O3Title.text('Ozone (O3) Predictions');
O3div.append(O3Title);

// Create NO2div
var NO2div = $('<div id = "NO2div" ></div>');
const NO2thresholds = [25,200,200]
var NO2Title = $('<div id = "NO2title" ></div>');
NO2Title.text('Nitrogen dioxide (NO2) Predictions');
NO2div.append(NO2Title);

// Append divs to the mainDiv
$('#mainDiv').append(O3div);
$('#mainDiv').append(NO2div);

// Create legend O3
var legendO3 = $('<div class="legend" id="O3Legend"></div>'); // Added quotes around O3Legend
O3div.append(legendO3); // Append legendO3 to O3div

const legendItemsO3 = [
    { color: 'red', label: 'High Concentrations (Above 200 u/mg3)' },
    { color: 'orange', label: 'Medium Concentrations (Between 100 and 200 u/mg3)' },
    { color: 'green', label: 'Low Concentrations (Below 100 u/mg3)' }
];

// Iterate through legend items and append to the legend
legendItemsO3.forEach(item => {
    // Create the legend text container
    const legendText = $('<div class="legend-text"></div>');

    // Create the dot
    const dot = $('<div class="dot"></div>').addClass(item.color);

    // Create the label
    const label = $('<span></span>').text(item.label);

    // Append the dot and label to the legend text container
    legendText.append(dot).append(label);

    // Append the legend text container to the legend
    legendO3.append(legendText); // Changed from $('#O3Legend') to legendO3
});

// Create legend NO2
var legendNO2 = $('<div class="legend" id="NO2Legend"></div>'); // Added quotes around O3Legend
NO2div.append(legendNO2); // Append legendO3 to O3div

const legendItemsNO2 = [
    { color: 'red', label: 'High Concentrations (Above 200 u/mg3)' },
    { color: 'orange', label: 'Medium Concentrations (Between 25 and 200 u/mg3)' },
    { color: 'green', label: 'Low Concentrations (Below 25 u/mg3)' }
];

// Iterate through legend items and append to the legend
legendItemsNO2.forEach(item => {
    // Create the legend text container
    const legendText = $('<div class="legend-text"></div>');

    // Create the dot
    const dot = $('<div class="dot"></div>').addClass(item.color);

    // Create the label
    const label = $('<span></span>').text(item.label);

    // Append the dot and label to the legend text container
    legendText.append(dot).append(label);

    // Append the legend text container to the legend
    legendNO2.append(legendText); // Changed from $('#O3Legend') to legendO3
});


// Function to fetch data
const requestData = async (target_column) => {
    try {
        let response = await $.ajax({
            url: "http://127.0.0.1:8000/get_data",
            method: "POST",
            contentType: "application/json",  // Specify content type
            data: JSON.stringify({
                target_column: target_column,  // Use the correct key
            }),
        });
        return response;
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;  // Rethrow or handle accordingly
    }
};

// Call requestData function and update O3div
const targetColumnO3 = "O3";  
const targetColumnNO2 = "NO2";
requestData(targetColumnO3).then(response => {
    const valuesToPlot = response.data
    createPlot(valuesToPlot, O3thresholds, targetColumnO3);
    console.log(valuesToPlot)
}).catch(error => {
    // Handle error   
    console.log(error)
});

requestData(targetColumnNO2).then(response => {
    const valuesToPlot = response.data
    createPlot(valuesToPlot, NO2thresholds, targetColumnNO2);
    console.log(valuesToPlot)
}).catch(error => {
    // Handle error
    console.log(error)
});



