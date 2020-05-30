from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DetailView

from App_Post.forms import CommentForm
from App_Login.models import Follow
from App_Post.models import Posts, LoveReact


# Create your views here.
@login_required
def home(request):
    following_list = Follow.objects.filter(follower=request.user)
    post = Posts.objects.filter(author__in=following_list.values_list('following'))
    loved_post = LoveReact.objects.filter(user=request.user)
    loved_post_list = loved_post.values_list('post', flat=True)
    diction = {'title': 'Home', 'posts': post, 'loved_post_list': loved_post_list}
    if request.method == "GET":
        search = request.GET.get('search_bar', ' ')
        result_get = User.objects.filter(username__icontains=search)
        diction.update({'result': result_get, 'title': 'Home | search'})
    return render(request, "App_Post/home.html", context=diction)


@login_required
def loved(request, pk):
    post = Posts.objects.get(pk=pk)
    already_loved = LoveReact.objects.filter(post=post, user=request.user)
    if not already_loved:
        like_post = LoveReact(post=post, user=request.user)
        like_post.save()
    return HttpResponseRedirect(reverse('App_Post:home'))


@login_required
def no_loved(request, pk):
    post = Posts.objects.get(pk=pk)
    already_loved = LoveReact.objects.filter(post=post, user=request.user)
    already_loved.delete()
    return HttpResponseRedirect(reverse('App_Post:home'))


@login_required
def comment_post(request, pk):
    post = Posts.objects.get(pk=pk)
    print("Post from comment form: ", post)
    comment_form = CommentForm()
    if request.method == 'POST':
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('App_Post:home'))

    return render(request, "App_Post/details_post.html", context={'comment_form': comment_form, 'post': post})


@login_required
def details_my_picture(request, pk):
    post = Posts.objects.get(pk=pk)
    diction = {'post': post}
    return render(request, "App_Post/details_my_post.html", context=diction)


@login_required
def delete_mypost(request, pk):
    post_delete = Posts.objects.get(pk=pk)
    post_delete.delete()
    return HttpResponseRedirect(reverse('App_Post:details_my_picture'), kwargs={'pk': pk})


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Posts
    fields = ['post_image', 'caption', ]
    template_name = 'App_Post/edit_post.html'

    def get_success_url(self):
        return reverse_lazy('App_Post:details_my_picture', kwargs={'pk': self.object.pk})


class PostDetails(LoginRequiredMixin, DetailView):
    model = Posts
    template_name = 'App_Post/details_my_post.html'
