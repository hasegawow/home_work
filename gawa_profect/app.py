from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from flask_login import UserMixin, LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
db = SQLAlchemy(app)
login_manager = LoginManager()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=True)
    body = db.Column(db.String(300), nullable=True)
    creates_at = db.Column(db.DateTime, nullable=False, default = datetime.now(pytz.timezone('Asia/Tokyo')).replace(second=0, microsecond=0))

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/create', methods = ["GET","POST"])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        post = Post(title=title, body=body)

        db.session.add(post)
        db.session.commit()
        return redirect('/')

    else:
        return render_template('create.html')


@app.route('/<int:id>/update', methods = ["GET","POST"])
def update(id):
    id = Post.query.get(id)
    if request.method == 'POST':
        id.title = request.form.get('title')
        id.body = request.form.get('body')

        db.session.commit()
        return redirect('/')

    else:
        return render_template('update.html', post=id)


@app.route('/<int:id>/delete')
def delete(id):
    id = Post.query.get(id)

    db.session.delete(id)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

