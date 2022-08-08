from init import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Month, Expense
from forms import LoginForm, RegistrationForm, SavingsForm, ExpenseForm, EditForm
from nltk import flatten
import datetime

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def home():
    savingsForm = SavingsForm()
    expenseForm = ExpenseForm()
    editForm = EditForm()

    if current_user.is_authenticated:
        getMonth = Month.query.filter_by(user_id=current_user.id).all()
        expenses = Expense.query.filter_by(month_id=getMonth[-1].month_id).all()
        if current_user.salary is None:
            savingsForm.savings_date.data = datetime.datetime(2023, 1, 1)
        elif savingsForm.salary.data is None:
            savingsForm.salary.data = current_user.salary
            savingsForm.savings_goal.data = current_user.savings_goal
            savingsForm.savings_date.data = current_user.savings_date

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

        if expenseForm.expense_submit.data and expenseForm.validate_on_submit():
            expense = Expense(expenseForm.expense_type.data, expenseForm.cost.data, datetime.datetime.now(), getMonth[-1].month_id)
            db.session.add(expense)
            db.session.commit()
            return(redirect(url_for('home')))
        elif len(expenseForm.errors.items()) > 0:
            errorList = flatten(list(expenseForm.errors.values()))
            for error in errorList:
                flash(error, 'danger')
            return(redirect(url_for('home')))

        if editForm.update_expense.data and editForm.validate_on_submit():
            expense = Expense.query.get(editForm.expense_id.data)
            expense.expense_type = editForm.expense_type.data
            expense.cost = editForm.cost.data
            db.session.commit()
            flash ('Expense Updated', 'primary')
            return(redirect(url_for('home')))
        elif editForm.remove_expense.data and editForm.validate_on_submit():
            expense = Expense.query.get(editForm.expense_id.data)
            db.session.delete(expense)
            db.session.commit()
            flash ('Expense Deleted', 'primary')
            return(redirect(url_for('home')))
        elif len(editForm.errors.items()) > 0:
            errorList = flatten(list(editForm.errors.values()))
            for error in errorList:
                flash(error, 'danger')
            return(redirect(url_for('home')))

        return render_template('authenticated_home.html', savingsForm = savingsForm, expenseForm = expenseForm, editForm = editForm, expenses = expenses)
    else:
        savingsForm.savings_date.data = datetime.datetime(2023, 1, 1)
        if savingsForm.validate_on_submit():
            flash('You Must Log In First!', 'danger')
            return redirect(url_for('login'))
        elif len(savingsForm.errors.items()) > 0:
            flash('You Must Log In First!SS', 'danger')
            return redirect(url_for('login'))
        return render_template('home.html', savingsForm = savingsForm, expenseForm = expenseForm, editForm = editForm)

@app.route('/expensesheets', methods=['GET', 'POST'])
@login_required
def expensesheets():
    if current_user.is_authenticated:
        if request.method == 'POST':
            print ('test')
        #if 'monthSelect' in locals():
            #getMonth = Month.query.filter_by(month=monthSelect, user_id=current_user.id).first()
        #else:
            #getMonth = Month.query.filter_by(month=monthSelect, user_id=current_user.id).all()
        #expenses = Expense.query.filter_by(month_id=getMonth.month_id).all()



        return render_template('expensesheets.html')
    else:
        return render_template('expensesheets.html')

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
            monthcheck = Month.query.filter_by(user_id=current_user.id).all()
            if monthcheck[-1].month.strftime("%Y-%m") != datetime.datetime.now().strftime("%Y-%m"):
                month = Month(month=datetime.datetime.now(),
                              user_id=current_user.id)
                db.session.add(month)
                db.session.commit()
            flash('Welcome ' + current_user.name + '!', 'primary')
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = 'home'
            return redirect(url_for(next))
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
        user = User(name=form.name.data,
                    email=form.email.data,
                    password=form.password.data)
        month = Month(month=datetime.datetime.now(),
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
