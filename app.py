from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] =  True
app.config['SECRET_KEY'] = "dfdvknerot34iuh4t39hi"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """redirect to shows list of all users in db"""
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def new_user():
    """show form to collect info for a new user"""
    return render_template('add_user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """add a new user to db and redirect to users"""
    
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    image_url = request.form["imageurl"]
    if image_url == "":
        new_user  = User(first_name=first_name, last_name=last_name)
    else:
        new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id)
    return render_template("user_details.html", user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """show form to update a user's info"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user_post(user_id):
    """update a user's info using the form input"""
    user = User.query.get_or_404(user_id)

    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    image_url = request.form["imageurl"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect(f'/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """delete a user from db using the id"""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect(f'/users')



# POST ROUTES

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """show form to collect info for a new post"""
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """add a new post to db and redirect to user"""
    
    title = request.form["title"]
    content = request.form["content"]

    new_post  = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show details about a post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template("post_details.html", post=post, user=user)

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """delete a post from db using the id"""
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()
    return redirect(f'/users')

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """show form to update a user's info"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_post(post_id):
    """update a user's info using the form input"""
    post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f'/users')