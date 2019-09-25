from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import (
    Paginator,
    EmptyPage, PageNotAnInteger,
)

import redis

from common.decorators import ajax_required
from actions.utils import create_action

from .forms import ImageCreateForm
from .models import Image

redis_inst = redis.StrictRedis(host=settings.REDIS_HOST,
                               port=settings.REDIS_PORT,
                               db=settings.REDIS_DB)


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully.')

            create_action(request.user, 'bookmarked image', new_item)

            return redirect(new_item.get_absolute_url())

    else:
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  { 'section': 'images',
                    'form'   : form })


@login_required
def image_list(request):
    # images = Image.objects.all()
    images = Image.objects.order_by('-total_likes')

    paginator = Paginator(images, 8)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      { 'section': 'images',
                        'images' : images })

    return render(request,
                  'images/image/list.html',
                  { 'section': 'images',
                    'images' : images })


def image_detail(request, image_id, slug):
    image = get_object_or_404(Image, id=image_id, slug=slug)

    total_views = redis_inst.incr(f'image:{image.id}:views')  # image:X:Y as key
    redis_inst.zincrby('image_ranking', image.id, 1)

    return render(request,
                  'images/image/detail.html',
                  { 'section'    : 'images',
                    'image_inst' : image,
                    'total_views': total_views })


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')  # get(IMAGE_ID_PASSED_IN_BY_ROUTES)
    action = request.POST.get('action')

    if image_id and action:
        try:
            image_inst = Image.objects.get(id=image_id)
            if action == 'like':
                image_inst.users_like.add(request.user)
                create_action(request.user, 'likes', image_inst)
            elif action == 'unlike':
                image_inst.users_like.remove(request.user)
            else:
                raise SystemError("HOLY FUCK action")

            return JsonResponse({ 'status': 'ok' })

        except Exception:
            raise SystemError("HOLY FUCK id+action")

    return JsonResponse({ 'status': 'ko' })


@login_required
def image_ranking(request):
    image_rankin = redis_inst.zrange('image_ranking', 0, -1,
                                     desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_rankin]

    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

    return render(request,
                  'images/image/ranking.html',
                  { 'section'    : 'images',
                    'most_viewed': most_viewed })
