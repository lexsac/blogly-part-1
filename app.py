from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, get_posts_list


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_of_users():
    """Shows list of users in db"""
    return redirect('/users')

@app.route('/users')
def show_all_users():
    """Shows list of users in db"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_by_id(user_id):
    """Shows user by user_id"""
    found_user = User.query.get_or_404(user_id)
    found_user_id = user_id
    return render_template("user_detail.html", found_user=found_user, found_user_id=found_user_id)

@app.route('/users/new')
def new_users_form():
    """"""
    return render_template('users_form.html')

@app.route('/users/new', methods=["POST"])
def add_new_user():
    """Retrieves form data, adds to database"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def edit_user_by_id(user_id):
    """"""
    found_user = User.query.get_or_404(user_id)
    return render_template('user_detail_edit.html', found_user=found_user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def commit_edit_user_by_id(user_id):
    """"""
    found_user = User.query.get_or_404(user_id)
    return render_template('user_detail_edit.html', found_user=found_user)

@app.route('/users/<int:user_id>/delete')
def delete_user_by_id(user_id):
    """"""
    found_user = User.query.get_or_404(user_id)
    db.session.delete(found_user)
    db.session.commit()
    
    return redirect('/users')
