from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .forms import PostForm, UserForm
from .models import Post


from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.
def index(request):
    my_phone = [
        {
            'name' : 'Koki Okano',
            'address' : '123 Hello St. Los Angeles, CA 9102',
            'phone': '111-222-3333'
        },
    ]
    context = {'posts': my_phone}
    return render(request, 'blog/index.html', context )

def posts(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'page_title': 'PHONEBOOK'
    }
    return render(request, 'blog/posts.html', context)

def registerPage(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()

        user = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")

        context = {'username': user}
        template = render_to_string('blog/emailtemplate.html', context)

        email_message = EmailMessage(
            'Welcome to my Django phonebook',  # subject line
            template, # body
            settings.EMAIL_HOST_USER,
            [email]
        )

        email_message.fail_silently = False
        email_message.send()

        return redirect('blog-login')
    context = {
        'form': form
    }
    return render(request, 'blog/register.html', context)


@login_required(login_url='blog-login')
def createPost(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }   
    return render(request, 'blog/createpost.html', context)

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username") # comes from the name attribute in the html tag
        password = request.POST.get("password1")

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            print(f'{user} is logged in')
            return redirect('blog-index')
    return render(request, 'blog/login.html')


@login_required(login_url='blog-login')
def logoutUser(request):
    logout(request)
    return redirect('blog-login')