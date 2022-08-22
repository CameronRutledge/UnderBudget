var total_cost = 0;
// Function for the creation of Google Pie Chart.
var pie_chart_array = [['Expense Type', 'Cost'], ['Housing', 0], ['Transportation', 0], ['Food', 0], ['Entertainment', 0], ['Misc.', 0]];
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
  // Reads each expense in month sheet, grabbing the expense type and cost.
  for (expense = 0; expense < expense_types.length; expense++) {
    var expense_type = expense_types[expense].getAttribute('value');
    var expense_cost = parseInt(expense_costs[expense].getAttribute('value').replace(/,/g, ''));
    total_cost += expense_cost
    expense_types[expense].value = expense_type;
    // Sorts all expenses into proper categorization for pie chart array.
    pie_chart_array.forEach(function(chart_piece){
      if (chart_piece[0] == expense_type) {
        chart_piece[1] += expense_cost
      }
    });
  }
  console.log((salary / 12))
  console.log(save_amount)
  if (typeof(save_amount) == 'undefined') {
    $("#month_overview").text(`You spent $${total_cost} in ${month_overview}.`);
  } else {
    $("#month_overview").text(`You have spent $${total_cost.toLocaleString('en-US')} in ${month_overview} so far. Be sure to keep this month's expenses below $${Math.round(((salary / 12) - save_amount)).toLocaleString('en-US')}.`);
  }
  google.charts.load("current", {packages:["corechart"]});
  google.charts.setOnLoadCallback(drawPieChart);
});
$(window).resize(function(){
  drawPieChart();
});
