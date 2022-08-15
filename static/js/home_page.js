function displaySavings(salary, savings_goal, start_date, savings_date){
  if (salary != '' && savings_goal != '') {
    var savedate = savings_date.split('-')
    var printGoalDate = new Date(savedate[0], savedate[1] - 1)
    printGoalDate = printGoalDate.toLocaleString([], {
      month: 'long', year: 'numeric'
    })
    var printStartDate = start_date.toLocaleString([], {
      month: 'long', year: 'numeric'
    })
    console.log(printStartDate)
    var months = (savedate[0] - start_date.getFullYear()) * 12;
    months -= start_date.getMonth();
    months += parseInt(savedate[1]) - 1;
    var save_amount = Math.round((savings_goal / months)*100)/100;
    var save_percent = Math.round((save_amount / (salary / 12)) * 10000)/100;
    $(".displaySavings").text(`In order to save $${savings_goal} by ${printGoalDate}, you will need to save $${save_amount} every month, which is ${save_percent}% of your monthly salary.`);
  } else {
    $(".displaySavings").text('Input your annual salary, the total amount you want to save, and your goal deadline, to determine your monthly savings goal.');
  }
}
$(document).ready(function(){
  var salary = $('#salary').val()
  var savings_goal = $('#savings_goal').val()
  var savings_date = $('#savings_date').val()
  if (typeof start_date == 'undefined') {
    start_date = new Date()
  } else {
    start_date = new Date(start_date[0], start_date[1])
  }
  displaySavings(salary, savings_goal, start_date, savings_date)
  $('.calculate').change(function(){
    console.log($(this).val())
    if ($(this).attr('id') == 'salary') {
      salary = $(this).val()
    } else if ($(this).attr('id') == 'savings_goal') {
      savings_goal = $(this).val()
    } else {
      savings_date = $(this).val()
    }
    displaySavings(salary, savings_goal, start_date, savings_date)
  });
});
