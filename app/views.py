from app import app
from flask import render_template, request, url_for, redirect, flash
from app.models import Blogs,Admin
from app import db
from flask_login import current_user, login_user, logout_user, login_required
import click

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blogs')
def blogs():
    page = request.args.get('page', 1, type=int)
    blogs = Blogs.query.order_by(Blogs.timestamp.desc()).paginate(page, 8, False)
    next_url = url_for("blogs", page=blogs.next_num)\
            if blogs.has_next else None
    prev_url = url_for("blogs", page=blogs.prev_num)\
            if blogs.has_prev else None
    return render_template('blogs.html', blogs = blogs.items, next_url = next_url, prev_url = prev_url)

@app.route('/life')
def life():
    page = request.args.get('page', 1, type=int)
    blogs = Blogs.query.filter_by(category = 1).paginate(page, 8, False)
    next_url = url_for("blogs", page=blogs.next_num)\
            if blogs.has_next else None
    prev_url = url_for("blogs", page=blogs.prev_num)\
            if blogs.has_prev else None
    return render_template('blogs.html', blogs = blogs.items, next_url = next_url, prev_url = prev_url)

@app.route('/code')
def code():
    page = request.args.get('page', 1, type=int)
    blogs = Blogs.query.filter_by(category = 0).paginate(page, 8, False)
    next_url = url_for("blogs", page=blogs.next_num)\
            if blogs.has_next else None
    prev_url = url_for("blogs", page=blogs.prev_num)\
            if blogs.has_prev else None
    return render_template('blogs.html', blogs = blogs.items, next_url = next_url, prev_url = prev_url)


@app.route('/blog/<blog_id>')
def read_blog(blog_id):
    blog = Blogs.query.get_or_404(blog_id)
    return render_template('read_blog.html', blog = blog)


@app.route('/delete_blog/<int:blog_id>',methods = ['POST'])
def delete_blog(blog_id):
    blog = Blogs.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('blogs'))

@app.route('/new_blog',methods = ['GET', 'POST'])
def new_blog():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        category = request.form['category']
        blog = Blogs(title = title, body = body, category = category)
        db.session.add(blog)
        db.session.commit()
        flash("Success!")
        return redirect(url_for('blogs'))
    return render_template('new_blog.html')


@app.route('/login',methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blogs'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash("Invalid input.")
        admin = Admin.query.filter_by(username = request.form['username']).first()
        if username == admin.username and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('blogs'))
        flash("账户或密码错误")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Goodbye')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.cli.command()
@click.option('--username', prompt = True)
@click.option('--password', prompt = True)
def admin(username, password):
    """Create user."""
    db.create_all()
    admin = Admin.query.first()
    user = Admin(username = username, name="Catfly")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo('Done.')

