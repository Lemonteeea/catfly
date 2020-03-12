from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blogs')
def blogs():
    blogs = ['00000','11111','22222','33333','44444','55555','66666','77777','88888','99999']
    return render_template('blogs.html',blogs=blogs)
