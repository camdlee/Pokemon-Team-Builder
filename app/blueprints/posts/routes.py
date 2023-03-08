# ----- IMPORTS ------
from flask import render_template, request, flash, redirect, url_for
from app.blueprints.posts.forms import PostForm
from app.models import Post
from app.blueprints.posts import posts
from flask_login import current_user, login_required


# ------- ROUTES ------

# ------ Registration Page ------
@posts.route('/create_post', methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        # Grabbing our form data and storing into a dict
        new_post_data ={
            'img_url': form.img_url.data,
            'title': form.title.data,
            'caption': form.caption.data,
            'user_id': current_user.id
        }

        # Create instance of User
        new_post = Post()
        
        # Implementing values from our form data for our instance
        new_post.from_dict(new_post_data)

        # Save to our database
        new_post.save_to_db()

        flash('You have successfully made a post!', 'success')
        return redirect(url_for('posts.view_posts'))
    return render_template('create_post.html', form=form)



#----- View All posts ------
@posts.route('/view_posts', methods=['GET'])
@login_required
def view_posts():
    posts = Post.query.all()
    return render_template('view_posts.html', posts=posts)