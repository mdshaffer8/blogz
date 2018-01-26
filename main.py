from flask import Flask, request, redirect, render_template, url_for, session, flash
from app import app, db
from models import Blogpost, User
from hashutils import make_password_hash, check_password_hash

app.secret_key = 'c2_8xit&vcwu@skn4ff'



@app.before_request
def require_login():
    allowed_routes = ['login', 'allposts', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session and '/static/' not in request.path:
        return redirect('/login')


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/allposts')
def allposts():

    if not request.args:
        posts = Blogpost.query.order_by(Blogpost.timestamp.desc()).all()
        return render_template('allposts.html', posts=posts)

    elif request.args.get('id'):
        user_id = request.args.get('id')
        post = Blogpost.query.filter_by(id=user_id).first()
        return render_template('post.html', post=post)
    
    elif request.args.get('user'):
        user_id = request.args.get('user')
        user = User.query.filter_by(id=user_id).first()
        posts = Blogpost.query.filter_by(owner_id=user_id).all()
        return render_template('user.html', posts=posts, user=user)


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
    return redirect('/allposts')


@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()
        user_length = len(username)
        pw_length = len(password)

        if existing_user:
            flash('User already exists.', 'error')
            return redirect("/signup")

        if not username:
            flash('Must enter a Username', 'error')
            errors = True

        if not password:
            flash('Must enter a Password', 'error')
            errors = True
        
        if user_length < 3:
            flash('Username must be at least 3 characters', 'error')
            errors = True
        
        if pw_length < 3:
            flash('Password must be at least 3 characters', 'error')
            errors = True

        if verify_password != password:
            flash('Passwords must match', 'error')
            errors = True
            
        else:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

        if errors:
            return redirect("/signup")

    return render_template('signup.html')



if __name__ == '__main__':
    app.run()