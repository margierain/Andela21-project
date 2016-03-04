import os
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from ..model import User, Post, Role, Permission, Comment # import classses from model.py
from .form import (PostForm,AdminProfile,CommentForm)# import forms from form,py
from app.decorators import admin_required, permission_required
from flask import current_app, abort
from werkzeug import secure_filename

# this part is good
@main.route('/user/<name>')
def user(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all() 
    page = request.args.get('page', 1, type=int) 
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
                                    page, per_page=current_app.config['JOKENIA_POSTS_PER_PAGE'],
                                    error_out=False)  
    return render_template('main/user.html', user=user, posts=posts, pagination=pagination)

@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'

@main.route('/create_store', methods=['GET', 'POST'])
@login_required
def create_store():
    form = PostForm()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
                                    page, per_page=current_app.config['JOKENIA_POSTS_PER_PAGE'],
                                    error_out=False)
    posts = pagination.items
    if form.validate_on_submit():
         
        file = request.files['uploadPhotoes']
        
        filename=None
        if file and file.filename.split('.')[-1] in ['jpeg','png','jpg']:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        post= Post(product=form.product.data, short_description=form.short_description.data,
                                Long_description=form.Long_description.data,uploadPhotoes=filename,
                                price=form.price.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash("There are errors in your form")
        return redirect(url_for('main.index'))
    else:
        flash('Product has been added')
    return render_template('main/create_store.html', form=form, posts=posts,pagination=pagination )

@main.route('/post/<int:id>',methods=['GET', 'POST'])
def post(id):

    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['JOKENIA_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['JOKENIA_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('main/post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)

    

   

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author: 
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        file = request.files['uploadPhotoes']
        
        filename=None
        if file and file.filename.split('.')[-1] in ['jpeg','png','jpg']:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        post.product = form.product.data
        post.short_description = form.short_description.data
        post.Long_description = form.Long_description.data
        post.uploadPhotoes = filename
        post.price = form.price.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
       
        return redirect(url_for('main.user',name=current_user.name))
       

    form.product.data = post.product
    form.short_description.data = post.short_description
    form.Long_description.data = post.Long_description
    form.price.data =  post.price
    return render_template('main/edit_post.html', form=form)

@main.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
    page, per_page=current_app.config['JOKENIA_POSTS_PER_PAGE'],
    error_out=False)
    posts = pagination.items
        
    return render_template('main/index.html', posts=posts,pagination=pagination )
