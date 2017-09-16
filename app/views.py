
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required  
from django.core.paginator import Paginator

from django.views.decorators.csrf import ensure_csrf_cookie


from app.forms import BootstrapAuthenticationForm, RegisterForm
from app.models import User, Post, Comment

from datetime import datetime


# this is the view for register
def registerUser(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'GET':
        user_form = RegisterForm()
        return render(request, 
            'app/register.html',
            {'form': user_form,
            'title':'Register',
            'year':datetime.now().year,
            })

    elif request.method == 'POST':

        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            User.objects.create(username = user_form.cleaned_data["username"], password=user_form.cleaned_data["password"])
            return redirect("home")

        else:
            return render(request, 
            'app/register.html',
            {'form': user_form,
            'title':'Register',
            'year':datetime.now().year,
            })


# this is the view for login
def loginUser(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        user_form = BootstrapAuthenticationForm()
        return render(request, 
            'app/login.html',
            {'form': user_form,
            'title':'Log in',
            'year':datetime.now().year,
            })

    elif request.method == 'POST':
        user_form = BootstrapAuthenticationForm(request.POST)
        if user_form.is_valid():
            user = authenticate(request, username=user_form.cleaned_data["username"], password=user_form.cleaned_data["password"])
        if user is not None:
            login(request, user)
            return redirect("home")
        
        else:
            return render(
                request,
                'app/index.html',
                {
                    'form': user_form,
                    'title': "Log in",
                    'year':datetime.now().year,
                })


# this is the view for creating a new post, using the markdown format
@login_required
def submitPost(request):
    if request.method == "GET":
        return render(
                request,
                'app/submitPost.html',
                {
                    'title': "Submit Post",
                    'year':datetime.now().year,
                })
    elif request.method == "POST":
        if request.user.is_authenticated():
            Post.objects.create(
                title = request.POST["title"],
                body = request.POST["content"],
                category = request.POST["category"],
                user = request.user
                )

        return redirect("home")




# method to assist the display of 2 colmuns of categories
def GetCategory():
    result = list(Post.objects.values('category').distinct())
    return result[int(len(result)/2):], result[:int(len(result)/2)] 


# index, home page
def home(request):
    assert isinstance(request, HttpRequest)

    pageNo = 1
    
    all_posts = Post.objects.select_related().all().order_by('-timestamp')
    pagination = Paginator(all_posts, 3)
    posts = pagination.page(1).object_list

    categoryLeft, categoryRight = GetCategory()

    return render(
        request,
        'app/index.html',
        
        {
            'posts': posts,
            'pageNo': pageNo,
            'categoryLeft' : categoryLeft,
            'categoryRight' : categoryRight,
            'title':'Home Page',
            'year':datetime.now().year,
        })


# this is the view for ajax result generating
# using ajax to do the partial refresh of (previous/next list of posts)
def renderPost(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":

        action = request.POST["action"]
        pageNo = request.POST["pageNo"]

        if action == "previous":
            newPageNo = int(pageNo) + 1  
        elif action == "next":
            newPageNo = int(pageNo) - 1  
        else:
            newPageNo = 1
    
        if newPageNo < 1:
            newPageNo = 1

        all_posts = Post.objects.select_related().all().order_by('-timestamp')
        pagination = Paginator(all_posts, 3)

        if newPageNo > pagination.num_pages:
            newPageNo = newPageNo - 1

        posts = pagination.page(newPageNo).object_list

        return render(request, 'app/renderPost.html', 
                               {'posts' : posts, 
                                'pageNo' : newPageNo})





# this is the view for showing a specific post
def showPost(request, postId):
    assert isinstance(request, HttpRequest)

    selectedPost=Post.objects.select_related().all().filter(id = postId).first()
    Comments=Comment.objects.select_related().all().filter(post__id = postId).all().order_by('-timestamp')

    categoryLeft, categoryRight = GetCategory()

    return render(request,
        'app/post.html',
        {
        'title' : "Post",
        'post' : selectedPost, 
        'categoryLeft' : categoryLeft,
        'categoryRight' : categoryRight,
        'year':datetime.now().year,
        'Comments' : Comments}
    )


# this is the view to handle the comments submitted
@login_required
def createComment(request):
    comment = request.POST["comment"]
    postId = request.POST["postId"]

    Comment.objects.create(body = comment
            ,user_id = request.user.id
            ,post_id = int(postId))

    return redirect(reverse('showPost', args=(postId,)))





# this is the serach function for title
def search(request):
    assert isinstance(request, HttpRequest)

    search = request.GET.get("search", None)
    pageNumber = request.GET.get("pageNumber", None)
    if pageNumber is None:
        pageNumber = 1
    else:
        pageNumber = int(pageNumber)

    categoryLeft, categoryRight = GetCategory()
    
    all_posts = Post.objects.select_related().filter(title__icontains=search).all().order_by('-timestamp')
    pagination = Paginator(all_posts, 3)
    paginate = pagination.page(pageNumber)

    return render(request, 'app/search.html', 
                  {'title': "Search",
                   'search':search, 
                   'paginate':paginate,
                   'categoryLeft' : categoryLeft, 
                   'categoryRight' : categoryRight, 
                   'year':datetime.now().year
                   })

# this is the serach function for category
def searchCategory(request, category):
    assert isinstance(request, HttpRequest)

    pageNumber = request.GET.get("pageNumber", None)
    if pageNumber is None:
        pageNumber = 1
    else:
        pageNumber = int(pageNumber)

    categoryLeft, categoryRight = GetCategory()
    
    all_posts = Post.objects.select_related().filter(category=category).all().order_by('-timestamp')
    pagination = Paginator(all_posts, 3)
    paginate = pagination.page(pageNumber)

    return render(request, 'app/searchCategory.html', 
                  {'title': "Search Category",
                   'category':category, 
                   'paginate':paginate,
                   'categoryLeft' : categoryLeft, 
                   'categoryRight' : categoryRight, 
                   'year':datetime.now().year
                   })

# this is the serach function for author
def searchAuthor(request, author):
    assert isinstance(request, HttpRequest)

    pageNumber = request.GET.get("pageNumber", None)
    if pageNumber is None:
        pageNumber = 1
    else:
        pageNumber = int(pageNumber)

    categoryLeft, categoryRight = GetCategory()
    
    all_posts = Post.objects.select_related().filter(user__username=author).all().order_by('-timestamp')
    pagination = Paginator(all_posts, 3)
    paginate = pagination.page(pageNumber)

    return render(request, 'app/searchAuthor.html', 
                  {'title': "Search Author",
                   'author':author, 
                   'paginate':paginate,
                   'categoryLeft' : categoryLeft, 
                   'categoryRight' : categoryRight, 
                   'year':datetime.now().year
                   })


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        
        {
            'title':'About',
            'message':'Django Blog App',
            'year':datetime.now().year,
        })
    
