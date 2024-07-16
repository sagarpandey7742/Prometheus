from flask import render_template, url_for, flash, redirect, request
from app.forms import SignUpForm, LoginForm
from app.models import User
from app import app, db, bcrypt

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
    form = LoginForm()
    if form.validate_on_submit():
        flash("Welcome " + form.email.data + "  :)", 'success')
        return redirect(url_for('home'))
    elif request.method == 'POST':
        flash("Invalid username or password", 'danger')
    return render_template('login.html', title='Prometheus | Login', form=form)

