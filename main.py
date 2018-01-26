from flask import Flask, request, redirect, render_template, url_for, session, flash
from app import app, db
from models import Blogpost, User
from hashutils import make_password_hash, check_password_hash

app.secret_key = 'c2_8xit&vcwu@skn4ff'


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/allposts')
def allposts():
    posts = Blogpost.query.order_by(Blogpost.timestamp.desc()).all()
    return render_template('allposts.html', posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':

        owner = User.query.filter_by(username=session['username']).first()
        title = request.form['title']
        content = request.form['content']

        post = Blogpost(title=title, content=content, owner=owner)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('allposts', id=post.id))

    return render_template('newpost.html')


@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User does not exist.", 'error')
            return redirect('/login')
        if not check_password_hash(password, user.password_hash):
            flash("Password is incorrect. Please try again.", 'error')
            return redirect('/login')
        else:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        
    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['username']
    flash("You are now logged out.")
    return redirect('/login')


@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('User already exists.', 'error')
            return redirect('/signup')

    return render_template('signup.html')



if __name__ == '__main__':
    app.run()