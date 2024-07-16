from flask import render_template, url_for, flash, redirect, request
from app.forms import SignUpForm, LoginForm
from app.models import User
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created for " + form.username.data + "  :)", 'success')
        return redirect(url_for('login'))
    elif request.method == 'POST':
        flash("Please correct the errors in the form.", 'danger')
    return render_template('signup.html', title='Prometheus | Sign Up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Welcome Back!!", 'success')
            return render_template('home.html', username=user.username, email=user.email, hashed_password=user.password)
        else:
            flash("Invalid email or password", 'danger')
    return render_template('login.html', title='Prometheus | Login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("Logged Out Successfully", 'info')
    return redirect(url_for('login'))
