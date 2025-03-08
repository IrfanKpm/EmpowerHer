from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def signup(request):
    """
    Handles user registration (signup) with manually created HTML form.
    Redirects authenticated users to the home page.
    """
    if request.user.is_authenticated:
        return redirect('home')  # Redirect authenticated users to the home page

    if request.method == "POST":
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate form data
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)  # Automatically log in the user after signup
        messages.success(request, "Account created successfully!")
        return redirect('home')  # Redirect to the home page after successful signup

    return render(request, 'signup.html')

def user_login(request):
    """
    Handles user login with manually created HTML form.
    Redirects authenticated users to the home page.
    """
    if request.user.is_authenticated:
        return redirect('home')  # Redirect authenticated users to the home page

    if request.method == "POST":
        # Retrieve form data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log in the user
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')  # Redirect to login page after logout

# Restrict pages to logged-in users
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='login')
def jobs(request):
    return render(request, 'jobs.html')

@login_required(login_url='login')
def safety(request):
    return render(request, 'safety.html')

@login_required(login_url='login')
def learning(request):
    return render(request, 'learning.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Discussion, Reply

@login_required(login_url='login')
def community(request):
    discussions = Discussion.objects.all().order_by('-created_at')

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            Discussion.objects.create(user=request.user, title=title, content=content)
            return redirect('community')

    return render(request, 'community.html', {'discussions': discussions})

@login_required(login_url='login')
def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    replies = discussion.replies.all().order_by('created_at')

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Reply.objects.create(user=request.user, discussion=discussion, content=content)
            return redirect('discussion_detail', discussion_id=discussion.id)

    return render(request, 'discussion_detail.html', {'discussion': discussion, 'replies': replies})
