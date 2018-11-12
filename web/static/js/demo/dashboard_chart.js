// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var canvas = document.getElementById('myAreaChart');
var data = {
    labels: [],
    datasets: [
        {
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(2,117,216,0.2)",
            borderColor: "rgba(2,117,216,0.2)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(2,117,216,0.2)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(2,117,216,0.2)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 5,
            pointHitRadius: 10,
            data: [],
        }
    ]
};

var option = {
	showLines: true,
  legend: {
    display: false
  }
};

var myLineChart = Chart.Line(canvas,{
	data:data,
  options:option
});
