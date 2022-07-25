from init import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Month, Expense
from forms import LoginForm, RegistrationForm, SavingsForm, ExpenseForm
from nltk import flatten
import datetime

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def home():
    savingsForm = SavingsForm()
    expenseForm = ExpenseForm()
    if current_user.is_authenticated:
        if current_user.salary is None:
            savingsForm.savings_date.data = datetime.datetime(2023, 1, 1)
        elif savingsForm.salary.data is None:
            savingsForm.salary.data = current_user.salary
            savingsForm.savings_goal.data = current_user.savings_goal
            savingsForm.savings_date.data = current_user.savings_date
        if savingsForm.validate_on_submit():
            current_user.salary = savingsForm.salary.data
            current_user.savings_goal = savingsForm.savings_goal.data
            current_user.savings_date = savingsForm.savings_date.data
            db.session.commit()
            return(redirect(url_for('home')))
        elif len(savingsForm.errors.items()) > 0:
            errorList = flatten(list(savingsForm.errors.values()))
            for error in errorList:
                flash(error, 'danger')
            return redirect(url_for('home'))

        return render_template('home.html', savingsForm = savingsForm, expenseForm = expenseForm)
    else:
        savingsForm.savings_date.data = datetime.datetime(2023, 1, 1)
        if savingsForm.validate_on_submit():
            flash('You Must Log In First!', 'danger')
            return redirect(url_for('login'))
        elif len(savingsForm.errors.items()) > 0:
            flash('You Must Log In First!', 'danger')
            return redirect(url_for('login'))
        return render_template('home.html', savingsForm = savingsForm, expenseForm = expenseForm)

@app.route('/expensesheets')
@login_required
def expensesheets():
    if current_user.is_authenticated:
        return render_template('expensesheets.html', test = current_user.email)
    else:
        return render_template('expensesheets.html', test = 'testers')

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
            monthcheck = Month.query.filter_by(user_id=user.id).all()
            if monthcheck[-1].month.strftime("%Y-%m") != datetime.datetime.now().strftime("%Y-%m"):
                month = Month(month=datetime.datetime.now(),
                              user_id=user.id)
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

        db.session.add(user)
        db.session.commit()
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
