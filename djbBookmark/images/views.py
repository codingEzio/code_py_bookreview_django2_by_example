from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import ImageCreateForm
from .models import Image


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

            return redirect(new_item.get_absolute_url())

    else:
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  { 'section': 'images',
                    'form'   : form })


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
            elif action == 'unlike':
                image_inst.users_like.remove(request.user)
            else:
                raise SystemError("HOLY FUCK action")

            return JsonResponse({ 'status': 'ok' })

        except Exception:
            raise SystemError("HOLY FUCK id+action")

    return JsonResponse({ 'status': 'ko' })


def image_detail(request, image_id, slug):
    image = get_object_or_404(Image, id=image_id, slug=slug)
    return render(request,
                  'images/image/detail.html',
                  { 'section'   : 'images',
                    'image_inst': image })
