from django.shortcuts import render, redirect
from .models import *      # from codetubeApp.models import *
from django.contrib import messages
import bcrypt


# Keep these for now so we can test front end visual ----------------------------------------
def index(request):
    return render(request, 'index.html')

def search(request):
    return render(request, 'search.html')

# def login_reg(request):
#     return render(request, 'login_reg.html')

# def dashboard(request):
#     return render(request, 'dashboard.html')

def new_video(request):
    return render(request, 'new_video.html')

def edit_video(request):
    return render(request, 'edit_video.html')

def play(request):
    return render(request, 'play.html')


# Login and Registration --------------------------------------------------------------------


def login_reg(request):
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


# Login - add if already logged in then what?
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
        else:
            messages.error(request,"Email was not found.")
    return redirect('/')


# Logout
def logout(request):
    request.session.clear()
    return redirect('/')


# Dashboard - Check if Logged in
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user,
        'all_videos': Video.objects.all(),
        # 'all_likes': Liked.objects.all()
    }
    return render(request,'dashboard.html', context)


# Videos and Likes --------------------------------------------------------------------------

# def index(request):
#     return render(request,'index.html')

# quote > video

# def add_quote(request):
#     if request.method=='POST':
#         errors = Quote.objects.quote_validate(request.POST)
#         if errors:
#             for error in errors:
#                 messages.error(request, errors[error])
#             return redirect('/success')
#         Quote.objects.create(author=request.POST['author'],quote=request.POST['quote'],user=User.objects.get(id=request.session['user_id']))
#         return redirect('/success')
#     return redirect('/success')

# def update(request,id):
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

# def liked(request):
#     if request.method=='POST':
#         Liked.objects.create(liked=request.POST['liked'], user=User.objects.get(id=request.session['user_id']), quote=request.POST['quote'])
#         context = {
#             'all_likes': Liked.objects.all.count()
#         }
#         return redirect('/success')

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

# def delete(request,id):
#     quote = Quote.objects.get(id=id)
#     quote.delete()
#     return redirect('/success')