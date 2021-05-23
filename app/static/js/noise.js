var chartT = new Highcharts.Chart({
    chart:{ renderTo : 'noise' },
    title: { text: 'PRN' + prn + ' noise' },
    series: [{
        showInLegend: false,
        data: []
    }],
    plotOptions: {
        line: {
            animation: false,
            dataLabels: { enabled: true }
        },
        series: { color: '#059e8a' }
    },
    xAxis: { type: 'time',
        dateTimeLabelFormats: { second: '%H:%M:%S' }
    },
    yAxis: {
        title: { text: 'Noise (dB)' }
    },
    credits: { enabled: false }
});

var count = 0;
var delay = 1;
setInterval(function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var x = count * delay;
            var y = parseFloat(this.responseText);
            count += 1;

            if (chartT.series[0].data.length > 40) {
                chartT.series[0].addPoint([x, y], true, true, true);
            } else {
                chartT.series[0].addPoint([x, y], true, false, true);
            }
        }
    };
    xhttp.open("GET", "/api/noise/" + prn, true);
    xhttp.send();
}, delay * 1000 );
