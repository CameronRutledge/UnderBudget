function displaySavings(salary, savings_goal, savings_date){
  if (salary != '' && savings_goal != '') {
    var today = new Date();
    var savedate = savings_date.split('-');
    var printDate = new Date(savedate[0], savedate[1] - 1)
    printDate = printDate.toLocaleString([], {
      month: 'long', year: 'numeric'

    })
    var months = (savedate[0] - today.getFullYear()) * 12;
    months -= today.getMonth();
    months += parseInt(savedate[1]) - 1;
    var save_amount = Math.round((savings_goal / months)*100)/100;
    var save_percent = Math.round((save_amount / (salary / 12)) * 10000)/100;
    $(".displaySavings").text(`In order to save $${savings_goal} by ${printDate}, you will need to save $${save_amount} every month, which is ${save_percent}% of your monthly salary.`);
  } else {
    $(".displaySavings").text('Input your annual salary, the total amount you want to save, and your goal deadline, to determine your monthly savings goal.');
  }
}
$(document).ready(function(){
  var salary = $('#salary').val()
  var savings_goal = $('#savings_goal').val()
  var savings_date = $('#savings_date').val()
  displaySavings(salary, savings_goal, savings_date)
  $('.calculate').change(function(){
    if ($(this).attr('id') == 'salary') {
      salary = $(this).val();
    } else if ($(this).attr('id') == 'savings_goal') {
      savings_goal = $(this).val();
    } else {
      savings_date = $(this).val();
    }
    displaySavings(salary, savings_goal, savings_date)
  });
});
