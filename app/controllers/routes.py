from app import app,db,lm
from flask import render_template,flash, redirect, url_for
from app.models.forms import LoginForm, Register
from flask_login import login_user, logout_user
from app.models.tables import User

@lm.user_loader
def load_user(id):
    print(f'Loading user with id: {id}')
    return User.query.filter_by(id = id).first()

@app.route('/index/<user>')
@app.route('/', defaults = {'user':None})
def index(user):
    return render_template('index.html', user = user)

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('feed'))
        else:
            flash('Invalid Login')

    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = Register()
    if form.validate_on_submit():
        if form.password.data == form.confirm_pass.data and len(form.password.data) >= 8:
            user = User(form.username.data,form.password.data,form.name.data,form.email.data)
            db.session.add(user)
            db.session.commit()
        elif form.password.data != form.confirm_pass.data:
            flash('Passwords are different')

    return render_template('signup.html', form= form)

@app.route('/feed')
def feed():
    return render_template('feed.html')
<<<<<<< HEAD

@app.route('/perfil/<user>')
def perfil(user):
    return render_template('perfil.html',user = user)
=======
>>>>>>> 3f554488346b6917707d68a7472548b21c841d4d
