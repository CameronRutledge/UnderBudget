from init import app, db
from flask import render_template, redirect, request, url_for, flash, abort, session
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Month, Expense
from forms import LoginForm, RegistrationForm, SavingsForm, ExpenseForm, EditForm
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from nltk import flatten

#Change date to the first of every month for month tracking.
def strip_date(date):
    return date.replace(day=1)

#Home Route: Page for posting savings goal and salary information as well as posting and updating expenses for the current month.
@app.route('/', methods=['GET', 'POST'])
def home():
    savingsForm = SavingsForm()
    expenseForm = ExpenseForm()
    editForm = EditForm()
    today = date.today()
    #Minimum and maximum values for savings goal selection.
    min = (today + relativedelta(years=1)).strftime('%Y-%m')
    max = (today + relativedelta(years=100)).strftime('%Y-%m')

    if current_user.is_authenticated:
        #Retrieve current month and expenses from database.
        getMonth = Month.query.filter_by(user_id=current_user.id, date=strip_date(today)).first()
        expenses = Expense.query.filter_by(month_id=getMonth.month_id).all()

        #Populate savingsForm with saved Salary, Goal, and Savings Date if posted, default to minimum goal if empty.
        if current_user.savings_date is None:
            savingsForm.savings_date.data = today + relativedelta(years=1)
        elif savingsForm.salary.data is None:
            savingsForm.salary.data = "{:,}".format(current_user.salary)
            savingsForm.savings_goal.data = "{:,}".format(current_user.savings_goal)
            savingsForm.savings_date.data = current_user.savings_date

        if request.method == 'POST':
            #Savings Form submission handling and error display.
            if savingsForm.savings_submit.data and savingsForm.validate_on_submit():
                current_user.salary = savingsForm.salary.data.replace(',', '')
                current_user.savings_goal = savingsForm.savings_goal.data.replace(',', '')
                current_user.savings_date = savingsForm.savings_date.data
                db.session.commit()
                return(redirect(url_for('home')))
            elif len(savingsForm.errors.items()) > 0:
                errorList = flatten(list(savingsForm.errors.values()))
                for error in errorList:
                    flash(error, 'danger')
                return(redirect(url_for('home')))

            #Requires user to post Savings Form before submitting expenses.
            if current_user.savings_date is None and expenseForm.expense_submit.data:
                flash ('Please input your annual salary, the total amount you want to save, and your goal deadline, before logging expenses', 'danger')
                return(redirect(url_for('home')))

            #Expense Form submission handling and error display.
            if expenseForm.expense_submit.data and expenseForm.validate_on_submit():
                expense = Expense(expenseForm.expense_type.data, expenseForm.cost.data.replace(',', ''), today, getMonth.month_id)
                db.session.add(expense)
                db.session.commit()
                return(redirect(url_for('home')))
            elif len(expenseForm.errors.items()) > 0:
                errorList = flatten(list(expenseForm.errors.values()))
                for error in errorList:
                    flash(error, 'danger')
                return(redirect(url_for('home')))

            #Edit Form submission handling and error display.
            if editForm.validate_on_submit():
                #If Update Button selected.
                if editForm.update_expense.data:
                    expense = Expense.query.filter_by(expense_id=editForm.expense_id.data).first()
                    expense.expense_type = editForm.expense_type.data
                    expense.cost = editForm.cost.data.replace(',', '')
                    db.session.commit()
                    flash ('Expense Updated', 'primary')
                    return(redirect(url_for('home')))
                #If Delete Button selected.
                elif editForm.remove_expense.data:
                    expense = Expense.query.filter_by(expense_id=editForm.expense_id.data).first()
                    db.session.delete(expense)
                    db.session.commit()
                    flash ('Expense Deleted', 'primary')
                    return(redirect(url_for('home')))
            elif len(editForm.errors.items()) > 0:
                errorList = flatten(list(editForm.errors.values()))
                for error in errorList:
                    flash(error, 'danger')
                return(redirect(url_for('home')))

        #Calculate user's savings progress and inform user if they are on pace to save on time.
        if current_user.savings_date is not None:
            start_date = [current_user.date_created.year, current_user.date_created.month - 1]
            #Calculate number of months to savings deadline.
            savingsPeriod = (current_user.savings_date.year - current_user.date_created.year) * 12 + current_user.savings_date.month - current_user.date_created.month
            #Calculate number of months that have passed.
            timeElapsed = (today.year - current_user.date_created.year) * 12 + today.month - current_user.date_created.month
            #Calculate number of months remaining till savings deadline.
            timeRemaining = savingsPeriod - timeElapsed
            #Calculate expected user savings for number of months elapsed.
            expectedSavings = (current_user.savings_goal / savingsPeriod) * timeElapsed
            #Compare actual user savings to expected
            if current_user.current_savings < expectedSavings:
                savingsDifference = 'You have saved ${} under your goal.'.format("{:,}".format(round(expectedSavings - current_user.current_savings, 2)))
            #Do not render savingsDifference if expecteSavings is 0 (month of account creation).
            elif expectedSavings == 0:
                savingsDifference = None
            elif current_user.current_savings == expectedSavings:
                savingsDifference = 'You are exactly on pace with your savings goal'
            else:
                savingsDifference = 'You have saved an estimated ${} so far. This is ${} ahead of schedule!'.format("{:,}".format(round(current_user.current_savings, 2)), "{:,}".format(round(current_user.current_savings - expectedSavings, 2)))

            #Page render with savingsDifference.
            return render_template('authenticated_home.html', savingsForm = savingsForm, expenseForm = expenseForm, editForm = editForm, expenses = expenses, min = min, max = max, savingsDifference = savingsDifference, current_savings = current_user.current_savings)
        else:
            #Unable to calculate savingsDifference render page without value.
            return render_template('authenticated_home.html', savingsForm = savingsForm, expenseForm = expenseForm, editForm = editForm, expenses = expenses, min = min, max = max, current_savings = current_user.current_savings)

    #Display for non-authenticated users.
    else:
        savingsForm.savings_date.data = today + relativedelta(years=1)
        if savingsForm.savings_submit.data:
            flash('You Must Log In First!', 'danger')
            return redirect(url_for('login'))

        return render_template('home.html', savingsForm = savingsForm, min = min, max = max)

#Expense Sheets Route: Page for viewing previous month expense sheets and expense category breakdown.
@app.route('/expensesheets', methods=['GET'])
@login_required
def expensesheets():
    #Requires user to post Savings Form before loading expensesheets, as there is no content to display for this user until they have posted at least 1 expense.
    if current_user.savings_date is None:
        flash ('Please input your annual salary, the total amount you want to save, and your goal deadline first', 'danger')
        return(redirect(url_for('home')))

    today = date.today()
    min = current_user.date_created.strftime('%Y-%m')
    max = today.strftime('%Y-%m')

    #Calculate number of months to savings deadline.
    savingsPeriod = (current_user.savings_date.year - current_user.date_created.year) * 12 + current_user.savings_date.month - current_user.date_created.month
    #Calculate number of months that have passed.
    timeElapsed = (today.year - current_user.date_created.year) * 12 + today.month - current_user.date_created.month
    #Calculate number of months remaining till savings deadline.
    timeRemaining = savingsPeriod - timeElapsed
    savingsProgress = ['You have saved ${} so far.'.format("{:,}".format(round(current_user.current_savings, 2))), 'This is ${} away from your goal of ${}.'.format("{:,}".format(round(current_user.savings_goal - current_user.current_savings, 2)), "{:,}".format(current_user.savings_goal)), 'You have {} months remaining before your Savings Goal Deadline.'.format(timeRemaining)]

    #Handles information sent from MonthSelect route, searches database for current month unless user has posted a month request.
    if session.get('monthSelect') is None:
        if session.get('monthError') is not None:
            flash(session['monthError'], 'danger')
            session['monthError'] = None
        getMonth = Month.query.filter_by(user_id=current_user.id, date=strip_date(today)).first()
    else:
        getMonth = Month.query.filter_by(month_id=session['monthSelect']).first()
        session['monthSelect'] = None
    expenses = Expense.query.filter_by(month_id=getMonth.month_id).all()

    #Collects all expense sheets a user has created, categorizing by expense type and the month the expense was posted. Used for bar chart display.
    allMonths = Month.query.filter_by(user_id=current_user.id).all()
    bar_chart_array = [['Month', 'Total Expenses', 'Housing', 'Transportation', 'Food', 'Entertainment', 'Misc'], ]
    for month in allMonths:
        expenseSum = Expense.query.filter_by(month_id=month.month_id).all()
        current_month = [month.date.strftime('%B %Y'), 0, 0, 0, 0, 0, 0]
        for expense in expenseSum:
            if expense.expense_type == 'Housing':
                current_month[1] += expense.cost
                current_month[2] += expense.cost
            elif expense.expense_type == 'Transportation':
                current_month[1] += expense.cost
                current_month[3] += expense.cost
            elif expense.expense_type == 'Food':
                current_month[1] += expense.cost
                current_month[4] += expense.cost
            elif expense.expense_type == 'Entertainment':
                current_month[1] += expense.cost
                current_month[5] += expense.cost
            elif expense.expense_type == 'Misc.':
                current_month[1] += expense.cost
                current_month[6] += expense.cost
        bar_chart_array.append(current_month)

    return render_template('expensesheets.html', expenses = expenses, min = min, monthSelected = getMonth.date.strftime('%Y-%m'), max = max, savingsProgress = savingsProgress, bar_chart_array = bar_chart_array)

#Month Select Route: Route for the handling of POSTs from Expense Sheets, selecting the month whose expenses will be displayed.
@app.route('/monthselect', methods=['POST'])
def monthselect():
    today = date.today()
    monthSelect = (datetime.strptime(request.form['monthSelect'], '%Y-%m')).date()
    getMonth = Month.query.filter_by(user_id=current_user.id, date=strip_date(monthSelect)).first()
    #If no month is found sets monthSelect to none and provides error code to Expense Sheets for flashing.
    if getMonth is None:
        session['monthSelect'] = None
        session['monthError'] = 'You do not have any expenses for the month of {}'.format(monthSelect.strftime('%B %Y'))
        return 'Failure'
    else:
        session['monthSelect'] = getMonth.month_id
        return 'Success'

#Logout Route: Logs user out.
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You Logged Out!', 'primary')
    return redirect(url_for('home'))

#Login Route: Handles user login requests and validates if correct information was posted.
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    #If user filled out all fields correctly further validation will be performed to confirm the user exists and the correct password was input.
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            monthCheck = strip_date(date.today())
            #Checks if the current month already possesses an expense sheet, if it does not a new month expense sheet is created.
            if Month.query.filter_by(user_id=current_user.id, date=monthCheck).first() is None:
                lastMonth = monthCheck - relativedelta(months=1)
                getMonth = Month.query.filter_by(user_id=current_user.id).all()
                #Collects and sums all expenses from the previous expense sheet, calculates how much the user saved that month.
                if getMonth is not None:
                    expenses = Expense.query.filter_by(month_id=getMonth[-1].month_id).all()
                    totalExpenses = 0
                    for expense in expenses:
                        totalExpenses += expense.cost
                    current_user.current_savings += (current_user.salary / 12) - totalExpenses

                month = Month(date=monthCheck,
                              user_id=current_user.id)
                db.session.add(month)
                db.session.commit()

            flash('Welcome {}!'.format(current_user.name), 'primary')
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('home')
            return redirect(next)
        else:
            flash('Invalid Email/Password', 'danger')
            return redirect(url_for('login'))

    elif len(form.errors.items()) > 0:
        errorList = flatten(list(form.errors.values()))
        for error in errorList:
            flash(error, 'danger')
        return redirect(url_for('login'))

    return render_template('login.html', form=form)

#Register Route: Handles user accout creation
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    #Validates that user filled out all fields correctly.
    if form.validate_on_submit():
        user = User(name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                date=date.today())
        db.session.add(user)
        db.session.commit()
        month = Month(date=strip_date(date.today()),
                user_id=user.id)
        db.session.add(month)
        db.session.commit()
        flash('Thank You For Registering! You Can Now Login!', 'primary')
        return redirect(url_for('login'))
    elif len(form.errors.items()) > 0:
        errorList = flatten(list(form.errors.values()))
        for error in errorList:
            flash(error, 'danger')
        return redirect(url_for('register'))

    return render_template('register.html', form=form)
