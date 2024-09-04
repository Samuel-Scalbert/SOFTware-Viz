// Fetch the data for the chart
fetch(`/api/line_chart`, {
    method: "GET"
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    // Extract datasets from the fetched data
    const createdData = data[0];
    const sharedData = data[1];
    const usedData = data[2];

    // Data for the chart
    const chartData = {
        labels: [2019, 2020, 2021, 2022, 2023],
        datasets: [
            {
                label: 'Used',
                data: usedData,
                fill: false,
                backgroundColor: "#6C9BCF",
                borderColor: "#6C9BCF",
                tension: 0
            },
            {
                label: 'Created',
                data: createdData,
                fill: false,
                backgroundColor: "#363949",
                borderColor: "#363949",
                tension: 0
            },
            {
                label: 'Shared',
                data: sharedData,
                fill: false,
                backgroundColor: "#677483",
                borderColor: "#677483",
                tension: 0
            }
        ]
    };

    // Configuration for the chart
    const chartConfig = {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                datalabels: {
                    display: false // Hides data labels
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: false,
                        text: 'Year'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: false,
                        text: 'Value'
                    }
                }
            }
        }
    };

    // Render the chart and store the instance
    const ctx = document.getElementById('lineChart').getContext('2d');
    window.myLineChart = new Chart(ctx, chartConfig); // Store the chart instance in a global variable
})
.catch(error => {
    console.error('Error:', error);
});