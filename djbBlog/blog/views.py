from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()  # fetch all if using `model = Post`
    context_object_name = 'posts'  # the name'd be used in the context (e.g. template)
    paginate_by = 3  # no more manual error handling, no need to form the query (?page)
    paginate_orphans = 1
    template_name = 'blog/post/list.html'  # the param being passed into need to change


def post_list(request):
    # Paging data & customization (/3, <1)
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3, orphans=1)  # 6->2p 7->2p 8->3p

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


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status='published')

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
    else:
        form = EmailPostForm

    return render(request, 'blog/post/share.html', { 'post': post,
                                                     'form': form })
