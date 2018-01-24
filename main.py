from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:kaibeans@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blogpost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route('/')
def index():
    posts = Blogpost.query.all()
    return render_template('blog.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)


@app.route('/newpost')
def newpost():
    return render_template('newpost.html')

def is_blank(x):
    if x:
        return False
    else:
        return True


# @app.route('/addpost', methods=['POST'])

# def user_errors():

#     title = request.form['title']
#     content = request.form['content']

#     title_error = ''
#     content_error = ''

#     if is_blank(title):
#         title_error = "Field cannot be blank"

#     if is_blank(content):
#         content_error = "Field cannot be blank"

#     if not title_error and not content_error:
#         post = Blogpost(title=title, content=content)

#         db.session.add(post)
#         db.session.commit()

#         return redirect(url_for('post', post_id=post.id))
#     else:
#         data = {'title':title, 'content':content}
#         return render_template('newpost.html', data = data, title_error=title_error, content_error=content_error)



@app.route('/addpost', methods=['POST'])
def addpost():

    title = request.form['title']
    content = request.form['content']

    post = Blogpost(title=title, content=content)

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('post', post_id=post.id))




if __name__ == '__main__':
    app.run()