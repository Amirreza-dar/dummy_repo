// <!DOCTYPE html>
// <html>
// <head>
//     <title>Pie Chart Example</title>
//     <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
// </head>
// <body>
//     <canvas id="myChart"></canvas>
//     <script>
        // var ctx = document.getElementById('myChart').getContext('2d');
        // var data = JSON.parse('{{ data | safe }}');
        // var labels = Object.keys(data);
        // var values = Object.values(data);
        
        // var myChart = new Chart(ctx, {
        //     type: 'pie',
        //     data: {
        //         labels: labels,
        //         datasets: [{
        //             data: values,
        //             backgroundColor: ['Red', 'Blue', 'Yellow'] // Example colors
        //         }]
        //     }
        // });
//     </script>
// </body>
// </html>
// external.js
// import Chart from 'chart.js/auto';

// Your chart initialization code here
document.addEventListener('DOMContentLoaded', function() {

    categories.forEach(function(cat, index) {

        var ctx = document.getElementById('pieChart' + index).getContext('2d');
        console.log(categories, chartData, chartSizes, chartColors);
        new Chart(ctx, {
            // TODO: find why it can't find Chart function
            type: 'pie',
            data: {
                labels: cat,
                datasets: [{
                    data: chartData[index],
                    backgroundColor: chartColors[index]
                }]
            },
            options: {
                maintainAspectRatio: false,
                responsive: false
            }
        });


    });
});

