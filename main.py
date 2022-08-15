from init import app, db
from flask import render_template, redirect, request, url_for, flash, abort, session
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Month, Expense
from forms import LoginForm, RegistrationForm, SavingsForm, ExpenseForm, EditForm, DateForm
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from nltk import flatten

def strip_date(date):
    return date.replace(day=1)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def home():
    savingsForm = SavingsForm()
    expenseForm = ExpenseForm()
    editForm = EditForm()
    today = date.today()
    min = (today + relativedelta(years=1)).strftime('%Y-%m')
    max = (today + relativedelta(years=100)).strftime('%Y-%m')


    if current_user.is_authenticated:
        getMonth = Month.query.filter_by(user_id=current_user.id, date=strip_date(today)).first()
        expenses = Expense.query.filter_by(month_id=getMonth.month_id).all()
        if current_user.savings_date is None:
            savingsForm.savings_date.data = today + relativedelta(years=1)
        elif savingsForm.salary.data is None:
            savingsForm.salary.data = current_user.salary
            savingsForm.savings_goal.data = current_user.savings_goal
            savingsForm.savings_date.data = current_user.savings_date

        if current_user.savings_date is not None:
            start_date = [current_user.date_created.year, current_user.date_created.month - 1]
            #Calculate number of months to savings deadline
            savingsPeriod = (current_user.savings_date.year - current_user.date_created.year) * 12 + current_user.savings_date.month - current_user.date_created.month
            #Calculate number of months that have passed
            timeElapsed = (today.year - current_user.date_created.year) * 12 + today.month - current_user.date_created.month
            #Calculate number of months remaining till savings deadline
            timeRemaining = savingsPeriod - timeElapsed
            #Calculate expected user savings for number of months elapsed
            expectedSavings = (current_user.savings_goal / savingsPeriod) * timeElapsed
            #Compare actual user savings to expected
            if current_user.current_savings < expectedSavings:
                savingsDifference = 'You have saved ${} under your goal.'.format(expectedSavings - current_user.current_savings)
            elif current_user.current_savings == expectedSavings:
                savingsDifference = 'You are exactly on pace with your savings goal'
            else:
                savingsDifference = 'You have saved ${} over your goal, good job!'.format(current_user.current_savings - expectedSavings)
            #Calculate how much user needs to save per month to meet their goal
            expectedMonth = (current_user.savings_goal - current_user.current_savings) / timeRemaining
            savingsPlan = 'You need to save at least ${} per month to meet your savings goal of {} by {}'.format(expectedMonth, current_user.savings_goal, current_user.savings_date)


        if request.method == 'POST':
            if savingsForm.savings_submit.data and savingsForm.validate_on_submit():
                current_user.salary = savingsForm.salary.data
                current_user.savings_goal = savingsForm.savings_goal.data
                current_user.savings_date = savingsForm.savings_date.data
                db.session.commit()
                return(redirect(url_for('home')))
            elif len(savingsForm.errors.items()) > 0:
                errorList = flatten(list(savingsForm.errors.values()))
                for error in errorList:
                    flash(error, 'danger')
                return(redirect(url_for('home')))

            if current_user.savings_date is None and expenseForm.expense_submit.data:
                flash ('Please input your annual salary, the total amount you want to save, and your goal deadline, before logging expenses', 'danger')
                return(redirect(url_for('home')))

            if expenseForm.expense_submit.data and expenseForm.validate_on_submit():
                expense = Expense(expenseForm.expense_type.data, expenseForm.cost.data, today, getMonth.month_id)
                db.session.add(expense)
                db.session.commit()
                return(redirect(url_for('home')))
            elif len(expenseForm.errors.items()) > 0:
                errorList = flatten(list(expenseForm.errors.values()))
                for error in errorList:
                    flash(error, 'danger')
                return(redirect(url_for('home')))

            if editForm.validate_on_submit():
                if editForm.update_expense.data:
                    expense = Expense.query.filter_by(expense_id=editForm.expense_id.data).first()
                    expense.expense_type = editForm.expense_type.data
                    expense.cost = editForm.cost.data
                    db.session.commit()
                    flash ('Expense Updated', 'primary')
                    return(redirect(url_for('home')))
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

        return render_template('authenticated_home.html', savingsForm = savingsForm, expenseForm = expenseForm, editForm = editForm, expenses = expenses, min = min, max = max, start_date = start_date, savingsDifference = savingsDifference, savingsPlan = savingsPlan)

    else:
        savingsForm.savings_date.data = today + relativedelta(years=1)
        if savingsForm.validate_on_submit():
            flash('You Must Log In First!', 'danger')
            return redirect(url_for('login'))
        elif len(savingsForm.errors.items()) > 0:
            flash('You Must Log In First!', 'danger')
            return redirect(url_for('login'))
        return render_template('home.html', savingsForm = savingsForm, min = min, max = max)

@app.route('/expensesheets', methods=['GET'])
@login_required
def expensesheets():
    dateForm = DateForm()
    today = date.today()
    min = (today + relativedelta(years=1)).strftime('%Y-%m')
    max = (today + relativedelta(years=100)).strftime('%Y-%m')
    if session.get('monthSelect') is not None:
        if session.get('monthError') is not None:
            flash(session['monthError'], 'danger')
            session['monthError'] = None
        getMonth = Month.query.filter_by(month_id=session['monthSelect']).first()
    else:
        getMonth = Month.query.filter_by(user_id=current_user.id, date=strip_date(today)).first()
    expenses = Expense.query.filter_by(month_id=getMonth.month_id).all()

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

    return render_template('expensesheets.html', dateForm = dateForm, expenses = expenses, min = min, monthSelected = getMonth.date.strftime('%Y-%m'), max = max, current_savings = current_user.current_savings, bar_chart_array = bar_chart_array)

@app.route('/monthselect', methods=['POST'])
def monthselect():
    today = date.today()
    monthSelect = (datetime.strptime(request.form['monthSelect'], '%Y-%m')).date()
    getMonth = Month.query.filter_by(user_id=current_user.id, date=strip_date(monthSelect)).first()
    if getMonth is None:
        getMonth = Month.query.filter_by(user_id=current_user.id, date=strip_date(today)).first()
        session['monthSelect'] = getMonth.month_id
        session['monthError'] = 'You do not have any expenses for the month of {}'.format(monthSelect.strftime('%B %Y'))
        return 'Success'
    else:
        session['monthSelect'] = getMonth.month_id
        return 'Success'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You Logged Out!', 'primary')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            monthCheck = strip_date(date.today())
            if Month.query.filter_by(user_id=current_user.id, date=monthCheck).first() is None:
                lastMonth = monthCheck - relativedelta(months=1)
                getMonth = Month.query.filter_by(user_id=current_user.id, date=lastMonth).first()
                if getMonth is not None:
                    expenses = Expense.query.filter_by(month_id=getMonth.month_id).all()
                    totalExpenses = 0
                    for expense in expenses:
                        totalExpenses += expense.cost

                    current_user.current_savings += (current_user.salary / 12) - totalExpenses

                month = Month(date=monthCheck,
                              user_id=current_user.id)
                db.session.add(month)
                db.session.commit()

            flash('Welcome {} !'.format(current_user.name), 'primary')
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.email.data == 'test@test.com':
            user = User(name=form.name.data,
                    email=form.email.data,
                    password=form.password.data,
                    date=date(2022,4,15))
            db.session.add(user)
            user.salary = 80000
            user.savings_goal = 100000
            user.savings_date = date(2024,12,1)
            user.current_savings = 11000
            db.session.commit()
            for months in range(4, 8):
                month = Month(date=date(2022,months,1),
                        user_id=user.id)
                db.session.add(month)
                db.session.commit()
                for expenses in ['Housing', 'Housing', 'Housing', 'Housing', 'Housing', 'Transportation', 'Food', 'Entertainment', 'Transportation', 'Transportation', 'Food', 'Entertainment', 'Misc.', 'Transportation', 'Food']:
                    expense = Expense(expenses, 200, date(2022,months,15), month.month_id)
                    db.session.add(expense)
                    db.session.commit()
        else:
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
        flash('Thank you for registering! You can now login!', 'primary')
        return redirect(url_for('login'))
    elif len(form.errors.items()) > 0:
        errorList = flatten(list(form.errors.values()))
        for error in errorList:
            flash(error, 'danger')
        return redirect(url_for('register'))

    return render_template('register.html', form=form)
