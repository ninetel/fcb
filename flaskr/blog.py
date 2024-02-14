from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, current_app
from flaskr.db import get_db 
import os

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
  
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created '
        ' FROM post p '
        ' ORDER BY created DESC'
    ).fetchall()
     
    return render_template('blog/index.html', posts=posts,tab_names='Home',website_name='BLOG')
A = os.getenv('FLASK_ADD')
print(os.getenv('FLASK_ADD')  )
print("00")
@bp.route(A, methods=('GET', 'POST'))
def create():
     
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body )'
                ' VALUES (?,   ?)',
                (title, body )
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html',tab_names="Create")

 
@bp.route('/<int:id>/display', methods=('GET', 'POST'))
def get_post(id ):
    post = get_db().execute(
        'SELECT p.id, title, body, created '
        ' FROM post p  '
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    

   

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    else:
        return render_template('blog/display.html', post=post,tab_names="View")    
 