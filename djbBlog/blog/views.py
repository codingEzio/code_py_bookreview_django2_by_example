from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post


def post_list(request):
    # Paging data & customization (/3, <1)
    object_list = Post.published.all()
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
                    'posts': posts })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  { 'post': post })
