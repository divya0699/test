from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import send_mail

from .forms import CommentForm
from .models import Blog



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog_list')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog_list')
    return render(request, 'blog/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def blog_list(request):
    blogs = Blog.objects.all()  
    paginator = Paginator(blogs, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blogs': page_obj,
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    comments = blog.comments.all()
    form = CommentForm()

    if request.method == 'POST':
        if 'text' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                comment.save()
                return redirect('blog_detail', id=id)
        
        if 'recipient_email' in request.POST:  # Check if the email field is present
            recipient_email = request.POST.get('recipient_email')
            send_blog_via_email(blog, recipient_email)  # Call the email sending function
            return redirect('blog_detail', id=id)

    context = {
        'blog': blog,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/blog_detail.html', context)


def blog_search(request):
    query = request.GET.get('q')
    if query:
        blogs = Blog.objects.filter(Q(tags__icontains=query))
    else:
        blogs = Blog.objects.all()
    return render(request, 'blog/blog_list.html', {'blogs': blogs, 'query': query})


def send_blog_via_email(blog, recipient_email):
    subject = f'Check out this blog: {blog.title}'
    message = f'Here is the content of the blog:\n\n{blog.content}\n\nTags: {blog.tags}'
    send_mail(subject, message, 'admin@gmail.com', [recipient_email])