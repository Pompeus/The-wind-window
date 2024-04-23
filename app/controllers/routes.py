from app import app,db,lm
from flask import render_template,flash, redirect, url_for,request
from app.models.forms import LoginForm, Register
from flask_login import login_user, logout_user, current_user
from app.models.tables import User, Post, Follow
from werkzeug.utils import secure_filename
import os

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

@app.route('/feed', methods = ['GET', 'POST'])
def feed():
    if not current_user.is_authenticated:
        flash('Please, Log in')
        return redirect(url_for('login'))

    follower_ids = [follow for follow in Follow.query.filter_by(follower_id = current_user.id).all()]

    follower_ids.append(current_user.id)

    
    posts = Post.query.filter(Post.user_id.in_(follower_ids)).all()
    
    return render_template('feed.html', posts = posts)

@app.route('/perfil/<user>')
def perfil(user):
    return render_template('perfil.html',user = user)

@app.route('/post', methods = ['POST'])
def post():
    content = request.form['content']
    if content:
        new_post = Post(user_id= current_user.id, content= content)
        db.session.add(new_post)
        db.session.commit()
    else:
        flash('Error, The post is empty')
    
    return redirect(url_for('feed'))

@app.route('/profile_image', methods = ['POST'])
def profile_image():
    if 'image' not in request.files:
        return ('Empty Image')
    
    file = request.files['image']
    if file.filename == '':
        flash('File name is Empty')

    if file:
        file_name = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],file_name)
        file.save(file_path)

    current_user.file_path = file_path

    db.session.add(current_user.file_path)
    db.session.commit()