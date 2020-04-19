from django.shortcuts import render
from .forms import CommentForm, PostForm, ReplyForm, ProfileForm
from django.shortcuts import render
from blog.models import Post, Comment, Category
from django.shortcuts import render, get_object_or_404
from blog.models import *
from django.contrib.auth.models import User 
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import UserForm, LoginForm
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
import datetime
from django.db.models import Q
import threading
import requests


def run_check():
    threading.Timer(600.0, run_check).start()
    a = requests.get('https://techb00k.herokuapp.com/')
    print(a)

def user_login(request):
    context = {}
    run_check()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username =  form.cleaned_data['username']
            password =  form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if request.GET.get('next', None):
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('user_success'))
            else:
                context['error'] = 'Invalid Username or Password!'
                context['msg'] = 'alert-danger'
                context['form'] = form
                return render(request, 'auth/login.html', context)
    else:
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})





@login_required(login_url='/login/')
def success(request):
    return HttpResponseRedirect(reverse('blog_index'))
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))



def user_add(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            pswrd = request.POST['password']
            usr = user_form.cleaned_data['username']
            user_form.save()
            user = authenticate(request, username=usr, password=pswrd)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('user_success'))   
        else:
            return render(request, 'login/add.html', {'user_from':user_form})
    else:
        user_form = UserForm()
        return render(request, 'login/add.html', {'user_form':user_form})


@login_required(login_url='/login/')
def blog_index(request):
    run_check()
    posts = Post.objects.all().order_by('-created_on')
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['cat']
            count = Category.objects.filter(name=a).count()
            post = Post(
            writer = request.user,
            body = form.cleaned_data['body'],
            title = form.cleaned_data['title'],
            )
            
            if count == 0:
                ct = Category(
                name =  form.cleaned_data['cat']  
                )
                ct.save()
            else:
                ct = Category.objects.get(name=a)
            post.save()
            post.categories.add(ct)
    context = {
        "posts": posts,
        'form' : form,
        'user' : request.user,
    }
    
    return render(request, "blog_index.html", context)



@login_required(login_url='/login/')
def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by('-created_on')
    total = posts.count()
    context = {
        "category": category,
        "posts": posts,
        'user' : request.user,
        'total' : total

    }
    return render(request, "blog_category.html", context)



@login_required(login_url='/login/')
def blog_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        post = None
    if post:
        
        dellink = ''
        editlink = ''
        print(type(post.title))
        if (str(request.user) == str(post.writer)) :
            dellink = 'Delete'
            editlink = 'Edit'
        form = CommentForm()
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(
                    author=request.user,
                    body=form.cleaned_data["body"],
                    post=post
                )
                comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')
        context = {
            'dellink': dellink,
            'editlink': editlink,
            "post": post,
            "comments": comments,
            "form": form,
            'user' : request.user,
        }
        return render(request, "blog_detail.html", context)
    else:
        return HttpResponseRedirect(reverse('blog_index'))





@login_required(login_url='/login/') 
def editpost(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST' :
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            a =  form.cleaned_data['cat']
            count = Category.objects.filter(name=a).count()
            if count == 0:
                ct = Category(
                name =  form.cleaned_data['cat']  
                )
                ct.save()
            else:
                ct = Category.objects.get(name=a)
            form.save()
            post.categories.add(ct)
            return HttpResponseRedirect(reverse('blog_detail', args=(post.pk,)))
        else:
            return render(request, 'editpost.html', {'form': form})
    else:
        form = PostForm(instance=post)
        print(form)
        return render(request, 'editpost.html', {'form': form})



@login_required(login_url='/login/')
def delpost(request, pk=None):
    Post.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('blog_index'))
    


@login_required(login_url='/login/') 
def cmt_detail(request, pk):
    try:
        comments = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        comments = None
    if comments:
        delcmt = ''
        editcmt = ''
        if (str(request.user) == str(comments.author) or str(request.user) == str(comments.post.writer)) :
            delcmt = 'Delete'
            if (str(request.user) == str(comments.author)):
                editcmt = 'Edit'
        form = ReplyForm()
        if request.method == 'POST':
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = ReplyComment(
                    reply_author=request.user,
                    reply_body=form.cleaned_data["reply_body"],
                    cmnt=comments
                )
                reply.save()

        replies = ReplyComment.objects.filter(cmnt=comments).order_by('-created_on')
        context = {
            'comments' : comments,
            'delcmt' : delcmt,
            'editcmt' : editcmt,
            'replies' : replies,
            'form' : form
        }
    
        return render(request, "cmt_detail.html", context)
    else:
        return HttpResponseRedirect(reverse('blog_index'))


@login_required(login_url='/login/') 
def editcmt(request, pk=None):
    cm = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=cm)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog_detail', args=(cm.post.pk,)))
        else:
            return render(request, 'editcmt.html', {'form': form})
    else:
        form = CommentForm(instance=cm)
        print(form)
        return render(request, 'editcmt.html', {'form': form})

        


@login_required(login_url='/login/')   
def delcmt(request, pk=None):
    try:
        cmt = get_object_or_404(Comment, pk=pk)
        a = cmt.post.pk
        cmt.delete()
        return HttpResponseRedirect(reverse('blog_detail', args=(a,)))
    except:
        return HttpResponseRedirect(reverse('blog_index'))



@login_required(login_url='/login/') 
def myprofile(request, uname):    
        
    pro = Profile.objects.get(user__username=uname)
    totalposts = Post.objects.filter(writer=uname).count()
    # print(pro.user)
    text = ''
    deluser = ''
    if (str(request.user) == str(pro.user)):
        text = 'Update'
        deluser = 'Delete'
    context = {
    'pro': pro,
    'totalposts': totalposts,
    'text' : text,
    'deluser' : deluser
        }
    print(pro.pro_pic)
    return render(request, "myprofile.html", context)
    

@login_required(login_url='/login/')
def myposts(request, u):
    try:
        post = Post.objects.filter(writer=u).order_by('-created_on')
        context = {
                'post' : post
            }
        return render(request, 'myposts.html', context)
    
    except:
    
        return HttpResponseRedirect(reverse('blog_index'))

@login_required(login_url='/login/')
def updateprofile(request, usr):
    prf = get_object_or_404(Profile, user__username=usr)
    if request.method == 'POST':
        pform = ProfileForm(request.POST, request.FILES, instance=prf)
        if pform.is_valid():
            pic = pform.cleaned_data['pro_pic']
            pform.save()

            return HttpResponseRedirect(reverse('myprofile', args=(prf.user,)))
        else:
            return render(request, 'profileupdate.html', {'pfrom':pform})
    else:
        pform = ProfileForm(instance=prf)
        return render(request, 'profileupdate.html', {'pform':pform})

@login_required(login_url='/login/')
def deluser(request, u):
    try:
        allpost = Post.objects.filter(writer=u)
        allpost.delete()
        usr = get_object_or_404(User, username=u)
        usr.delete()
        return HttpResponseRedirect(reverse('user_logout'))
    except:
        return HttpResponseRedirect(reverse('myprofile', args=(usr,)))

@login_required(login_url='/login/')
def search(request):
    query = request.GET.get('q', None)
    advance = query.split()
    error = ''
    msg = ''
    context = {}
    if query:
        udata = []
        data = []
        uresults = User.objects.filter(Q(username__icontains=query))
        results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(writer__icontains=query) | Q(categories__name__icontains=query))
        if results.count()==0 and uresults.count()==0:
            for adv in advance:
                ures = User.objects.filter(Q(username__icontains=adv))
                res = Post.objects.filter(Q(title__icontains=adv) | Q(body__icontains=adv) | Q(writer__icontains=adv) | Q(categories__name__icontains=adv))
                udata.append(ures)
                data.append(res)
            flag1= 'o'
            flag2 = 'k'
            for u in udata:
                if u.count()==0:
                    flag1 = 'ok'
                        
            for d in data:
                if d.count()==0:
                    flag2 = 'ok'
            if flag1==flag2:
                error = 'Sorry! No results found. Try with different keywords!'
                msg = 'alert-danger'
        context = {
        'results' : results,
        'uresults' : uresults,
        'udata' : udata,
        'data' : data,
        'error' : error,
        'msg' : msg
        }
        return render(request, 'results.html', context)
    else:
        return HttpResponseRedirect(reverse('blog_index'))


                