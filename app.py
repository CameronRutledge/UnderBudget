from Budget_Keeper import app, db
from Flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from Budget_Keeper.models import User
from Budget_Keeper.forms import LoginForm, RegistrationForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Successfully Logged In!')
            next = request.args.get('next')
            return redirect(url_for('home'))
        else:
            flash('Invalid Email/Password')
            return redirect(url_for('login'))

    elif form.validate_on_submit() == None:
        flash('Invalid Email/Password')
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
        flash('Thank you for registering! You can now login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
