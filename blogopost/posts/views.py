from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm, ProfileEdit
from .models import Comment, Follow, Group, Post, User
from .utils import make_pages


def index(request):
    posts = Post.objects.select_related('author')
    page_obj = make_pages(request, posts)
    context = {
        'posts': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()
    page_obj = make_pages(request, posts)
    context = {
        'group': group,
        'posts': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    page_obj = make_pages(request, posts)
    context = {
        'author': user,
        'posts': page_obj,
    }
    if request.user.is_authenticated:
        follow = Follow.objects.filter(user=request.user, author=user).exists()
        context['following'] = follow
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post_id)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('posts:profile', username=request.user.username)
    form = ProfileEdit(request.POST or None,
                       files=request.FILES or None,
                       instance=user.profile)
    if form.is_valid():
        user.profile.save()
        return redirect('posts:profile', username=user.username)
    return render(request,
                  'posts/edit_profile.html',
                  {'form': form})


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author.username)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post.pk)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id=post.pk)
    return render(request,
                  'posts/create_post.html',
                  {'form': form, 'is_edit': True})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.select_related('author').filter(
        author__following__user=request.user)
    page_obj = make_pages(request, posts)
    context = {
        'posts': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    exists = Follow.objects.filter(user=request.user, author=author).exists()
    if exists or request.user == author:
        return redirect('posts:profile', username=username)
    Follow.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    exists = Follow.objects.filter(user=request.user, author=author).exists()
    if not exists or request.user == author:
        return redirect('posts:profile', username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
