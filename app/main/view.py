import os
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from ..model import User, Post, Role, Permission # import classses from model.py
from .form import (PostForm,AdminProfile)# import forms from form,py
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


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
                                    page, per_page=current_app.config['JOKENIA_POSTS_PER_PAGE'],
                                    error_out=False)
    posts = pagination.items
    if form.validate_on_submit():
         
        file = request.files['uploadPhotoes']
        
        # for attr in dir(file):
        #     print attr
        filename=None
        if file and file.filename.split('.')[-1] in ['jpeg','png','jpg']:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        post= Post(product=form.product.data, short_description=form.short_description.data,
                                Long_description=form.Long_description.data,uploadPhotoes=filename,
                                price=form.price.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('Product has been added')
        return redirect(url_for('main.index'))
    else:
    
        flash("There are errors in your form")
    return render_template('main/index.html', form=form, posts=posts,pagination=pagination )

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('main/post.html', posts=[post])

   

@main.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
        not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.product = form.product.data
        post.short_description = form.short_description.data
        post.Long_description = form.Long_description.data
        post.uploadPhotoes = form.uploadPhotoes.data,
        post.price = form.price.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('edit_post'))
        return redirect(url_for('post', id=post.id))
    form.product.data = post.product
    form.short_description.data = post.short_description
    form.Long_description.data = post.Long_description
    form.uploadPhotoes.data = post.uploadPhotoes
    form.price.data =  post.price
    return render_template('main/edit_post.html', form=form)


