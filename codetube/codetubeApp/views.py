from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import random
import bcrypt
import logging
logger = logging.getLogger('django')


# General Routes ----------------------------------------------------------------------------

# Main Landing Page
def index(request):
    # so that we know whether to display log in or log out button
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = { 'user_id' : 'null' }
    all_videos = Video.objects.all()
    # randomize all_videos on landing page
    new_videos = list(all_videos)
    x = len(new_videos)
    random_videos = random.sample(new_videos, k=x)
    context = {
        'user' : user,
        'all_videos' : random_videos
    }
    return render(request, 'index.html', context)

# Search Page - filter results based on search term
def search(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = { 'user_id' : 'null' }
    all_videos = Video.objects.all()
    filtered_videos = all_videos.filter(title__icontains=request.POST['term'])
    context = {
        'user' : user,
        'all_videos': filtered_videos,
    }
    return render(request, 'search.html', context)

# Popular Videos
def popular_videos(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = { 'user_id' : 'null' }
    all_videos = Video.objects.all()
    popular_videos = all_videos.order_by("-views")
    context = {
        'user' : user,
        'all_videos': popular_videos,
    }
    return render(request, 'index.html', context)


# Testing Routes During Development ---------------------------------------------------------

# def search(request):
#     return render(request, 'search.html')

# def login_reg(request):
#     return render(request, 'login_reg.html')

# def dashboard(request):
#     return render(request, 'dashboard.html')

# def new_video(request):
#     return render(request, 'new_video.html')

# def edit_video(request):
#     return render(request, 'edit_video.html')

# def play(request):
#     return render(request, 'play.html')


# Login and Registration --------------------------------------------------------------------

# Login and Registration form page
def login_reg(request):
    if 'user_id' in request.session: # already logged in? re-route
        return redirect('/')
    return render(request, 'login_reg.html')

# Register a New User
def register(request):
    if request.method=='POST':
        errors = User.objects.reg_validate(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/login_reg')
        user_pw = request.POST['password']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hash_pw)
        request.session['user_id'] = new_user.id
        request.session['user_name'] = f"{new_user.first_name} {new_user.last_name}"
        return redirect('/dashboard')
    return redirect('/')

# Login
def login(request):
    if request.method=='POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/dashboard')
            else:
                messages.error(request,"Password is incorrect.")
                return redirect('/login_reg')
        else:
            messages.error(request,"Email was not found.")
            return redirect('/login_reg') # added this line, if email not found was sending them back to home
    return redirect('/')

# Logout - Clear Session
def logout(request):
    request.session.clear()
    return redirect('/')

# Dashboard - Check if Logged in, get like count and all videos
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/login_reg')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user,
        'all_videos': Video.objects.all(),
        'all_likes': Liked.objects.all(),
    }
    return render(request,'dashboard.html', context)


# Videos ------------------------------------------------------------------------------------

# Play video - every view incriments views by one, get like count
def play_video(request, id):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = { 'user_id' : 'null' }
    video = Video.objects.get(id=id)
    # replacing youtube browser url / link with an embeddable link allowing us to play with youtube controls.
    vid_url = video.video
    vid_updated = str.replace(vid_url, 'https://www.youtube.com/watch?v=', 'https://www.youtube.com/embed/')
    video.video = vid_updated
    # video view count
    video.views = video.views + 1
    video.save()
    all_videos = Video.objects.all()
    new_videos = list(all_videos)
    x = len(new_videos)
    random_videos = random.sample(new_videos, k=x)
    video_list = random_videos[0:10]
    logger.info(video_list)
    likes = 0
    # video likes
    all_likes = Liked.objects.all()
    for like in all_likes:
        if like.video == Video.objects.get(id=id):
            likes = likes + 1
    context = {
        'user' : user,
        'video' : video,
        'likes' : likes,
        'video_list': video_list
    }
    return render(request, 'play.html', context)

# New video form page
def new_video(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user,
    }
    return render(request, 'new_video.html', context)

# Create a new video
def create_video(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method=='POST':
        errors = Video.objects.video_validate(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/new_video')
        Video.objects.create(title=request.POST['title'],video=request.POST['video'],thumbnail=request.POST['thumbnail'],description=request.POST['description'],user=User.objects.get(id=request.session['user_id']))
        return redirect('/dashboard')
    return redirect('/new_video')

# Edit video form page
def edit_video(request, id):
    if 'user_id' not in request.session: 
        return redirect('/')
    video = Video.objects.get(id=id)
    if request.session['user_id'] != video.user.id:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user,
        'video' : Video.objects.get(id=id)
    }
    return render(request, 'edit_video.html', context)

# Update video
def update_video(request, id):
    if 'user_id' not in request.session: 
        return redirect('/')
    video = Video.objects.get(id=id)
    if request.session['user_id'] != video.user.id:
        return redirect('/')
    if request.method=='POST':
        errors = Video.objects.video_validate(request.POST) # create video validations same as update?
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect(f"/edit_video/{id}")
        video = Video.objects.get(id=id)
        video.title=request.POST['title']
        video.video=request.POST['video']
        video.thumbnail=request.POST['thumbnail']
        video.description=request.POST['description']
        video.save()
        return redirect('/dashboard')
    return redirect('/edit_video/<int:id>')

# Delete video
def delete_video(request, id):
    if 'user_id' not in request.session: 
        return redirect('/')
    video = Video.objects.get(id=id)
    if request.session['user_id'] != video.user.id:
        return redirect('/')
    video = Video.objects.get(id=id)
    video.delete()
    return redirect('/dashboard')


# Likes -------------------------------------------------------------------------------------

# Like video toggle
def like_video(request, id):
    if request.method=='POST':
        if 'user_id' not in request.session: 
            return redirect(f'/play/{id}')
        video = Video.objects.get(id=id)
        user = User.objects.get(id=request.session['user_id'])
        all_likes = Liked.objects.all()
        for like in all_likes:
            if like.video_id == video.id and like.user_id == user.id:
                video.likes = video.likes - 1
                video.views = video.views -1
                video.save()
                this_like = Liked.objects.get(id=like.id)
                this_like.delete()
                return redirect(f'/play/{id}')
        video.likes = video.likes + 1
        video.views = video.views -1
        video.save()
        Liked.objects.create(video=video, user=user)
        return redirect(f'/play/{id}')
    return redirect(f'/play/{id}')

# User liked videos
def user_liked(request):
    if 'user_id' not in request.session:
        return redirect('/login_reg')
    user = User.objects.get(id=request.session['user_id'])
    all_likes = Liked.objects.all()
    liked_videos = []
    for like in all_likes:
        if like.user_id == user.id:
            video = Video.objects.get(id=like.video_id)
            liked_videos.append(video)
    context = {
        'user': user,
        'all_likes': all_likes,
        'liked_videos': liked_videos
    }
    return render(request, 'user_liked.html', context)


# If you want to be able to update user, reference ------------------------------------------

# def account_page(request,id):
#     context = {
#         'user': User.objects.get(id=id)
#     }
#     return render(request,'edit_account.html',context)

# def user_page(request,id):
#     user = User.objects.get(id=id)
#     context = {
#         'user': user
#     }
#     return render(request,'user_page.html', context)

# Update a user if we wanted to add
# def update_user(request,id):
#     if request.method=='POST':
#         ## validations
#         errors = User.objects.update_validate(request.POST)
#         if errors:
#             for error in errors:
#                 messages.error(request, errors[error])
#             return redirect(f"/myaccount/{id}")
#         user = User.objects.get(id=id)
#         user.first_name=request.POST['first_name']
#         user.last_name=request.POST['last_name']
#         user.email=request.POST['email']
#         user.save()
#         request.session['user_name'] = f"{user.first_name} {user.last_name}"
#         return redirect('/success')
#     return redirect('/myaccount/<int:id>')