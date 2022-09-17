from django.shortcuts import render, redirect
from codetubeApp.models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    return render(request, 'search.html')

def login_reg(request):
    return render(request, 'login_reg.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def new_video(request):
    return render(request, 'new_video.html')

def edit_video(request):
    return render(request, 'edit_video.html')

def play(request):
    return render(request, 'play.html')




# Reference
from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        errors = User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        user_pw = request.POST['password']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hash_pw)
        request.session['user_id'] = new_user.id
        request.session['user_name'] = f"{new_user.first_name} {new_user.last_name}"
        return redirect('/success')
    return redirect('/')

def login(request):
    if request.method=='POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/success')
            else:
                messages.error(request,"Password is incorrect.")
        else:
            messages.error(request,"Email was not found.")
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')


def success(request):
    context = {
        'all_quotes': Quote.objects.all(),
        # 'all_likes': Like.objects.all()
    }
    return render(request,'success.html',context)

def add_quote(request):
    if request.method=='POST':
        errors = Quote.objects.quote_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/success')
        Quote.objects.create(author=request.POST['author'],quote=request.POST['quote'],user=User.objects.get(id=request.session['user_id']))
        return redirect('/success')
    return redirect('/success')
        
def update(request,id):
    if request.method=='POST':
        ## validations
        errors = User.objects.update_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect(f"/myaccount/{id}")
        user = User.objects.get(id=id)
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.email=request.POST['email']
        user.save()
        request.session['user_name'] = f"{user.first_name} {user.last_name}"
        return redirect('/success')
    return redirect('/myaccount/<int:id>')

def like(request):
    if request.method=='POST':
        Like.objects.create(like=request.POST['like'], user=User.objects.get(id=request.session['user_id']), quote=request.POST['quote'])
        context = {
            'all_likes': Like.objects.all.count()
        }
        return redirect('/success')

def account_page(request,id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request,'edit_account.html',context)

def user_page(request,id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request,'user_page.html', context)

def delete(request,id):
    quote = Quote.objects.get(id=id)
    quote.delete()
    return redirect('/success')