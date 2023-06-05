from flask import Blueprint, jsonify, session, request
from flask_login import login_required, current_user
from app.models import Post, User, PostImage, db, friendships, likes, Comment
from app.forms import PostForm
from .auth_routes import validation_errors_to_error_messages
from sqlalchemy.orm import joinedload
from sqlalchemy import or_


post_routes = Blueprint('posts', __name__)

## Get all posts - FINISHED
@post_routes.route("/")
# @login_required
def posts():
    """
    Query for all posts and returns then in a list of post dictionaries
    """
    # get the current user

    # posts = Post.query.all()
    # posts = Post.query.join(User).join(PostImage, isouter=True).options(joinedload(Post.post_images)).all()
    # return [{'post': post.to_dict(), 'user': post.user.to_dict(), 'postImages': [post.post_image.to_dict() for post.post_image in post.post_images] } for post in posts]


    #Grabs current user
    user = User.query.get(current_user.id)
    print('------------------queried user-----------', user)
    #Grabs current user posts
    user_posts = user.posts
    print('----------------user posts---------', user_posts)
    #Grabs current user friendships
    friends = user.friendships

    # friends_from_userA = user.friendships.filter(friendships.c.userA_id == user.id)
    # friends_from_userB = user.friendships.filter(friendships.c.userB_id == user.id)

    # friends = friends_from_userA.union_all(friends_from_userB).all()
    print('------------------queried friends-----------', friends)

    # for friend in friends:
    #     posts = friend.posts
    #     print('-----------posts-------------', posts)

    # posts = [friend.posts.to_dict() for friend in friends]


    # post_images = posts.post_images
    # print('--------------post_images--------', post_images)
    # post_comments = posts.comments
    # print('-----------post of the comments-------------', post_comments)

    # Put this in for loop
    # Grabs friend 1's posts
    # posts = friends[0].posts
    # print('-------------q_posts-----------', posts)
    # posts.append(user_posts)
    # print('-------------user posts-----------', user_posts)
    # posts_images = posts[0].post_images
    # print('-------------post images---------', posts_images)

    # post_comments = posts[0].comments

    # get curretn users friends

    #get ids of friends to filter by
    friend_ids = [user.id for user in friends]

    #get all posts of the friends of users order in desc order
    # post.query.filter(post.user_id)

    posts = Post.query \
        .join(User) \
        .join(PostImage, isouter=True) \
        .join(likes, Post.id == likes.c.post_id, isouter=True) \
        .options(joinedload(Post.post_images)) \
        .filter(User.id.in_(friend_ids))\
        .order_by(Post.created_at.desc())\
        .all()


    #  .join(Comment, Comment.post_id == Post.id, isouter=True) \
    #organize the data
    return_posts = []
    for post in posts:
        post_dic = {}

        post_dic.update(post.to_dict())
        post_dic.update({'user': post.user.to_dict()} )
        post_dic.update({'postImages': [post.post_image.to_dict() for post.post_image in post.post_images]})
        del post_dic['userId']
        post_likes = post.likes
        liked_by = [user.to_dict() for user in post_likes]
        post_dic['likes'] = len(post.likes)
        post_dic['liked_by'] = liked_by
        post_dic.update({'comments': [post.comment.to_dict() for post.comment in post.comments]})
        return_posts.append(post_dic)

    return return_posts

## Create New Post - FINISHED
@post_routes.route("/new", methods=['POST'])
@login_required
def create_post():
    """
    Create a post
    """
    form = PostForm()
    print(current_user)
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        new_post = Post(
            content = form.data['content'],
            user_id = current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post.to_dict()


## Delete A Post - NOT FINISHED/CHECKED
@post_routes.route("/<int:id>", methods=['DELETE'])
@login_required
def remove_post(id):
    """
    Delete a post
    """

    """
        1. Query the post id
        2. Check to see if the post_id matches the owner of the id? I guess we can do this in react
        3. Remove post
    """
    post = Post.query.get(id)
    if post:
        post.remove()
        return jsonify({'message': 'Post deleted successfully'})




## Get Single Post - CHECK THIS
@post_routes.route('/<int:id>')
@login_required
def single_post(id):
    """
    Query for a single post and returns it in a dictionary
    """
    post = Post.query\
        .filter_by(id=id)\
        .join(User)\
        .join(PostImage, isouter=True)\
        .options(joinedload(Post.post_images))\
        .join(likes, Post.id == likes.c.post_id, isouter=True) \
        .first()

    post_dic = {}

    post_dic.update(post.to_dict())
    post_dic.update({'user': post.user.to_dict()} )
    post_dic.update({'postImages': [post.post_image.to_dict() for post.post_image in post.post_images]})
    del post_dic['userId']
    post_likes = post.likes
    liked_by = [user.to_dict() for user in post_likes]
    post_dic['likes'] = len(post.likes)
    post_dic['liked_by'] = liked_by

    return post_dic

# TODO: Update Post

# TODO: Get User Posts
