var chart_array = [['Expense Type', 'Cost'], ['Housing', 0], ['Transportation', 0], ['Food', 0], ['Entertainment', 0], ['Misc.', 0]];
function drawChart() {
  console.log(chart_array)
  var data = google.visualization.arrayToDataTable(chart_array);
    var options = {
    title: 'Monthly Expenses',
    titleTextStyle: {
      color: '#FFFFFF',
      fontName: 'Lato',
      fontSize: 40,
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
  piechart.draw(data, options);
}
$(document).ready(function(){
  var expense_types = document.getElementsByClassName('type_display');
  var expense_costs = document.getElementsByClassName('cost_display');
  for (expense = 0; expense < expense_types.length; expense++) {
    var expense_type = expense_types[expense].getAttribute('value');
    var expense_cost = parseInt(expense_costs[expense].getAttribute('value'));
    expense_types[expense].value = expense_type;
    chart_array.forEach(function(chart_piece){
      if (chart_piece[0] == expense_type) {
        chart_piece[1] += expense_cost
      }
    });
  }
  google.charts.load("current", {packages:["corechart"]});
  google.charts.setOnLoadCallback(drawChart);
});
$(window).resize(function(){
  drawChart();
});
