function drawLineChart() {
  var data = google.visualization.arrayToDataTable(bar_chart_array);
    var options = {
    title: 'Monthly Expenses',
    titleTextStyle: {
      color: '#FFFFFF',
      fontName: 'Lato',
      fontSize: 30,
      bold: 'false'
    },
    backgroundColor: 'transparent',
    legend: 'bottom',
    legendTextStyle: {
      color: '#FFFFFF',
      fontName: 'Lato',
    },
    hAxis: {
      textStyle: {
        color: '#FFFFFF',
        fontName: 'Lato',
      }
    },
    vAxis: {
      format: 'currency',
      textStyle: {
        color: '#FFFFFF',
        fontName: 'Lato',
      }
    },
    lineWidth: 4,
    isStacked: true
  };
  var linechart = new google.visualization.LineChart(document.getElementById('barchart'));
  var formatter = new google.visualization.NumberFormat({prefix: '$'});
  formatter.format(data, 1);
  formatter.format(data, 2);
  formatter.format(data, 3);
  formatter.format(data, 4);
  formatter.format(data, 5);
  linechart.draw(data, options);
}
$(document).ready(function(){
  var monthSelect = $('.month_select').val()
  $('.month_select').change(function(){
    if ($(this).val() != monthSelect){
      $.ajax({
        url: '/monthselect',
        data: {"monthSelect": $(this).val()},
        type: 'POST',
        success: function (response) {
          window.location.reload()
        },
        error: function (error) {
          console.log(error);
        }
      });
    }
  });
  google.charts.load("current", {packages:["corechart"]});
  google.charts.setOnLoadCallback(drawLineChart);
});
$(window).resize(function(){
  drawLineChart();
});
