var pie_chart_array = [['Expense Type', 'Cost'], ['Housing', 0], ['Transportation', 0], ['Food', 0], ['Entertainment', 0], ['Misc.', 0]];
var total_cost = 0
function drawPieChart() {
  var data = google.visualization.arrayToDataTable(pie_chart_array);
    var options = {
    title: 'Current Month Expenses',
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
    is3D: true,
  };

  var piechart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
  var formatter = new google.visualization.NumberFormat({prefix: '$'});
  formatter.format(data, 1);
  piechart.draw(data, options);
}
$(document).ready(function(){
  var expense_types = document.getElementsByClassName('type_display');
  var expense_costs = document.getElementsByClassName('cost_display');
  var month_overview = $('#month_overview').text()
  for (expense = 0; expense < expense_types.length; expense++) {
    var expense_type = expense_types[expense].getAttribute('value');
    var expense_cost = parseInt(expense_costs[expense].getAttribute('value'));
    total_cost += expense_cost
    expense_types[expense].value = expense_type;
    pie_chart_array.forEach(function(chart_piece){
      if (chart_piece[0] == expense_type) {
        chart_piece[1] += expense_cost
      }
    });
  }
  $("#month_overview").text(`For the month ${month_overview} you have spent $${total_cost}.`);
  google.charts.load("current", {packages:["corechart"]});
  google.charts.setOnLoadCallback(drawPieChart);
});
$(window).resize(function(){
  drawPieChart();
});
