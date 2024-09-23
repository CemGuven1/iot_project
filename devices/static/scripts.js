// Helper function to limit data points to the last 20
function limitChartData(chart) {
    // Check if the labels and datasets exceed the maximum data points
    if (chart.data.labels.length > maxDataPoints) {
        chart.data.labels = chart.data.labels.slice(-maxDataPoints);
    }
    chart.data.datasets.forEach(dataset => {
        if (dataset.data.length > maxDataPoints) {
            dataset.data = dataset.data.slice(-maxDataPoints);
        }
    });
}


//time formatting
function formatTimestamp(timestamp) {
    const date = new Date(timestamp); // Convert timestamp to Date object
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Months are 0-indexed
      
    // Return formatted as MM/DD HH:MM:SS
    return `${month}/${day} ${hours}:${minutes}:${seconds}`;
    }
      

    
    // accel chart setup
    const accel_ctx = document.getElementById('AccelChart').getContext('2d');
    let AccelChart = new Chart(accel_ctx, {
        type: 'line',
        data: {
            labels: [], // This will be filled with timestamps
            datasets: [
                {
                    label: 'Acceleration X',
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    data: []  // This will be filled with acceleration_x values
                },
                {
                    label: 'Acceleration Y',
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    data: []  // This will be filled with acceleration_y values
                },
                {
                    label: 'Acceleration Z',
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    data: []  // This will be filled with acceleration_z values
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // This allows the chart to respect your custom height
            layout: {
                padding: {
                  left: 100,
                  right: 100,
                  top: 20,
                  bottom: 50
                }
              },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Device Acceleration Over Time'
                }
            }
        }
    });


    // gyro chart setup
    const gyro_ctx = document.getElementById('GyroChart').getContext('2d');
    let GyroChart = new Chart(gyro_ctx, {
        type: 'line',
        data: {
            labels: [], // This will be filled with timestamps
            datasets: [
                {
                    label: 'Gyro Position X',
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    data: []  // This will be filled with acceleration_x values
                },
                {
                    label: 'Gyro Position Y',
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    data: []  // This will be filled with acceleration_y values
                },
                {
                    label: 'Gyro Position Z',
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    data: []  // This will be filled with acceleration_z values
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // This allows the chart to respect your custom height
            layout: {
                padding: {
                  left: 100,
                  right: 100,
                  top: 20,
                  bottom: 50
                }
              },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Device Gyro Positions Over Time'
                }
            }
        }
    });


    // temp chart setup
    const temp_ctx = document.getElementById('TempChart').getContext('2d');
    let TempChart = new Chart(temp_ctx, {
        type: 'line',
        data: {
            labels: [], // This will be filled with timestamps
            datasets: [
                {
                    label: 'Temperature',
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    data: []  // This will be filled with acceleration_x values
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // This allows the chart to respect your custom height
            layout: {
                padding: {
                  left: 100,
                  right: 100,
                  top: 20,
                  bottom: 50
                }
              },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Device Temperature Over Time'
                }
            }
        }
    });


    // battery chart setup
    const battery_ctx = document.getElementById('BatteryChart').getContext('2d');
    let BatteryChart = new Chart(battery_ctx, {
        type: 'line',
        data: {
            labels: [], // This will be filled with timestamps
            datasets: [
                {
                    label: 'Battery',
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    data: []  // This will be filled with acceleration_x values
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // This allows the chart to respect your custom height
            layout: {
                padding: {
                  left: 100,
                  right: 100,
                  top: 20,
                  bottom: 50
                }
              },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Device Temperature Over Time'
                }
            }
        }
    });


// Chart Checkbox Dataset Visibility
function updateChartVisibility() {
    const accelXVisible = document.getElementById('toggle-accel-x').checked;
    const accelYVisible = document.getElementById('toggle-accel-y').checked;
    const accelZVisible = document.getElementById('toggle-accel-z').checked;
    const gyroXVisible = document.getElementById('toggle-gyro-x').checked;
    const gyroYVisible = document.getElementById('toggle-gyro-y').checked;
    const gyroZVisible = document.getElementById('toggle-gyro-z').checked;
    const tempVisible = document.getElementById('toggle-temp').checked;
    const batteryVisible = document.getElementById('toggle-battery').checked;

    AccelChart.data.datasets[0].hidden = !accelXVisible;
    AccelChart.data.datasets[1].hidden = !accelYVisible;
    AccelChart.data.datasets[2].hidden = !accelZVisible;

    GyroChart.data.datasets[0].hidden = !gyroXVisible;
    GyroChart.data.datasets[1].hidden = !gyroYVisible;
    GyroChart.data.datasets[2].hidden = !gyroZVisible;

    TempChart.data.datasets[0].hidden = !tempVisible;

    BatteryChart.data.datasets[0].hidden = !batteryVisible;

    AccelChart.update();
    GyroChart.update();
    TempChart.update();
    BatteryChart.update();
    }


// Event listeners for checkbox changes
document.getElementById('toggle-accel-x').addEventListener('change', updateChartVisibility);
document.getElementById('toggle-accel-y').addEventListener('change', updateChartVisibility);
document.getElementById('toggle-accel-z').addEventListener('change', updateChartVisibility);
document.getElementById('toggle-gyro-x').addEventListener('change', updateChartVisibility);
document.getElementById('toggle-gyro-y').addEventListener('change', updateChartVisibility);
document.getElementById('toggle-gyro-z').addEventListener('change', updateChartVisibility);
document.getElementById('toggle-temp').addEventListener('change', updateChartVisibility);
document.getElementById('toggle-battery').addEventListener('change', updateChartVisibility);

// Initialize the chart visibility on page load
document.addEventListener('DOMContentLoaded', updateChartVisibility);


function toggleChartVisibility(chartId) {
    const chartContainer = document.getElementById(chartId);
    if (chartContainer.style.display === 'none' || chartContainer.style.display === '') {
        chartContainer.style.display = 'block';
    } else {
        chartContainer.style.display = 'none';
    }
}

// Event listener for Acceleration Chart toggle button
document.getElementById('toggleAccelChart').addEventListener('click', function() {
    const chartContainerId = 'accelChartContainer';
    
    toggleChartVisibility(chartContainerId);
    const chartContainer = document.getElementById(chartContainerId);

    if (chartContainer.style.display === 'none') {
        this.innerHTML = '<i class="fas fa-tachometer-alt"></i> Show Acceleration Chart';
    } else {
        this.innerHTML = '<i class="fas fa-tachometer-alt"></i> Hide Acceleration Chart';
    }
});

// Event listener for Gyro Chart toggle button
document.getElementById('toggleGyroChart').addEventListener('click', function() {
    const chartContainerId = 'gyroChartContainer';
    
    toggleChartVisibility(chartContainerId);
    const chartContainer = document.getElementById(chartContainerId);

    if (chartContainer.style.display === 'none') {
        this.innerHTML = '<i class="fas fa-chart-line"></i> Show Gyro Chart';
    } else {
        this.innerHTML = '<i class="fas fa-chart-line"></i> Hide Gyro Chart';
    }
});

// Event listener for Temperature Chart toggle button
document.getElementById('toggleTempChart').addEventListener('click', function() {
    const chartContainerId = 'tempChartContainer';
    
    toggleChartVisibility(chartContainerId);
    const chartContainer = document.getElementById(chartContainerId);

    if (chartContainer.style.display === 'none') {
        this.innerHTML = '<i class="fas fa-thermometer-half"></i> Show Temperature Chart';
    } else {
        this.innerHTML = '<i class="fas fa-thermometer-half"></i> Hide Temperature Chart';
    }
});

// Event listener for Battery Chart toggle button
document.getElementById('toggleBatteryChart').addEventListener('click', function() {
    const chartContainerId = 'batteryChartContainer';
    
    toggleChartVisibility(chartContainerId);
    const chartContainer = document.getElementById(chartContainerId);

    if (chartContainer.style.display === 'none') {
        this.innerHTML = '<i class="fas fa-battery-half"></i> Show Battery Chart';
    } else {
        this.innerHTML = '<i class="fas fa-battery-half"></i> Hide Battery Chart';
    }
});



// Accordion menu logic
document.addEventListener("DOMContentLoaded", function() {
    const accordion = document.querySelector(".accordion");
    const panel = document.querySelector(".panel");

    accordion.addEventListener("click", function() {
        this.classList.toggle("active");

        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
});