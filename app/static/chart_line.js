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
    console.log(data); // Log the fetched data to verify its structure

    // Extract datasets from the fetched data
    const usedData = data[0];
    const createdData = data[1];
    const sharedData = data[2];

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

    // Render the chart
    const ctx = document.getElementById('lineChart').getContext('2d');
    new Chart(ctx, chartConfig);
})
.catch(error => {
    console.error('Error:', error);
});
