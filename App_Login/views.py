from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import CreateNewUser, EditUserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, Follow
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from App_Post.forms import PostForm


# Create your views here.
def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse('App_Login:login'))
    diction = {'title': 'Signup', 'form': form}
    return render(request, 'App_Login/signup.html', context=diction)


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user=user)
                return HttpResponseRedirect(reverse('App_Post:home'))
    diction = {'title': 'Login', 'form': form}
    return render(request, "App_Login/login.html", context=diction)


@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))


@login_required
def profile(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_obj = form.save(commit=False)
            post_obj.author = request.user
            post_obj.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    diction = {'form': form}
    return render(request, "App_Login/user.html", context=diction)


@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditUserProfile(instance=current_user)
    diction = {'title': 'Edit Profile', 'form': form}
    if request.method == "POST":
        form = EditUserProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditUserProfile(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, "App_Login/profile.html", context=diction)


@login_required
def searching_user(request, user_is):
    user_other = User.objects.get(username=user_is)
    already_follow = Follow.objects.filter(follower=request.user, following=user_other)
    if user_other == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, "App_Login/searching_user.html",
                  context={'user_other': user_other, 'already_follow': already_follow})


@login_required
def follow(request, user_is):
    following_user = User.objects.get(username=user_is)
    follower_user = request.user
    already_follow = Follow.objects.filter(follower=follower_user, following=following_user)
    if not already_follow:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()

    return HttpResponseRedirect(reverse('App_Login:searching_user', kwargs={'user_is': user_is}))


@login_required
def unfollow(request, user_is):
    following_user = User.objects.get(username=user_is)
    follower_user = request.user
    already_follow = Follow.objects.filter(follower=follower_user, following=following_user)
    if already_follow:
        already_follow.delete()
    return HttpResponseRedirect(reverse('App_Login:searching_user', kwargs={'user_is': user_is}))
