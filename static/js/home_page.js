var save_amount = 0
// Takes input of salary, savings goal, and savings date to calculate.
function displaySavings(salary, savings_goal, savings_date){
  if (isNaN(salary) || isNaN(savings_goal)) {
    $(".displaySavings").text('Input your annual salary, the total amount you want to save, and your goal deadline, to determine your monthly savings goal.');
  } else {
    var savedate = savings_date.split('-')
    var today = new Date()
    var printGoalDate = new Date(savedate[0], savedate[1] - 1)
    printGoalDate = printGoalDate.toLocaleString([], {
      month: 'long', year: 'numeric'
    })
    var savingsPeriod = (savedate[0] - today.getFullYear()) * 12;
    savingsPeriod -= today.getMonth();
    savingsPeriod += parseInt(savedate[1]) - 1;
    save_amount = Math.round(((savings_goal - current_savings) / savingsPeriod) * 100) / 100;
    var save_percent = Math.round((save_amount / (salary / 12)) * 10000)/100;
    $(".displaySavings").text(`In order to save $${savings_goal.toLocaleString('en-US')} by your goal of ${printGoalDate}, you will need to save $${save_amount.toLocaleString('en-US')} every month, which is ${save_percent}% of your monthly salary.`);
  }
}
$(document).ready(function(){
  var salary = parseInt($('#salary').val().replace(/,/g, ''))
  var savings_goal = parseInt($('#savings_goal').val().replace(/,/g, ''))
  var savings_date = $('#savings_date').val()
  displaySavings(salary, savings_goal, savings_date)
  // Runs function to read new salary, savings goal, or savings date vand calculate on update.
  $('.calculate').change(function(){
    if ($(this).attr('id') == 'salary') {
      salary = parseInt($(this).val().replace(/,/g, ''))
    } else if ($(this).attr('id') == 'savings_goal') {
      savings_goal = parseInt($(this).val().replace(/,/g, ''))
    } else {
      savings_date = $(this).val()
    }
    displaySavings(salary, savings_goal, savings_date)
  });

  // Not my code, sourced from https://stackoverflow.com/questions/31867551/html-input-type-number-thousand-separator. Reads input fields and parses string to add a comma for proper number formatting.
  var $input = $(".input" );
  $input.on( "keyup", function( event ) {
    // When user select text in the document, also abort.
    var selection = window.getSelection().toString();
    if ( selection !== '' ) {
      return;
    }
    // When the arrow keys are pressed, abort.
    if ( $.inArray( event.keyCode, [38,40,37,39] ) !== -1 ) {
      return;
    }
    var $this = $( this );
    // Get the value.
    var input = $this.val();
    var input = input.replace(/[\D\s\._\-]+/g, "");
        input = input ? parseInt( input, 10 ) : 0;
        $this.val( function() {
          return ( input === 0 ) ? "" : input.toLocaleString( "en-US" );
        } );
  });
});
