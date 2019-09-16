import os

from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

from taggit.models import Tag


class PostListView(ListView):
    queryset = Post.published.all()  # fetch all if using `model = Post`
    context_object_name = 'posts'  # the name'd be used in the context (e.g. template)
    paginate_by = 3  # no more manual error handling, no need to form the query (?page)
    paginate_orphans = 1
    template_name = 'blog/post/list.html'  # the param being passed into need to change


def post_list(request, tag_slug = None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # Paging data & customization (e.g. 6->2p 7->2p 8->3p)
    paginator = Paginator(object_list, 3, orphans=1)

    # localhost:8000/blog/?page=WHAT_U_SPECIFIED
    page = request.GET.get('page')  # get the current page number

    # get the data of specific page
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # if(not num) => first page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # if(num <= 0) => last page

    return render(request,
                  'blog/post/list.html',
                  { 'page' : page,
                    'posts': posts,
                    'tag'  : tag })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  { 'post'        : post,
                    'comments'    : comments,
                    'new_comment' : new_comment,
                    'comment_form': comment_form })


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email_from']}) " \
                f"recommends you reading {post.title}"
            message = f"Read '{post.title}' at {post_url}\n\n" \
                f"{cd['name']}'s comments: {cd['comments']}"

            send_mail(subject, message, os.environ['EMAIL_HOST_USER'], [cd['email_to']])
            sent = True

    else:
        form = EmailPostForm

    return render(request, 'blog/post/share.html', { 'post': post,
                                                     'form': form,
                                                     'sent': sent })
