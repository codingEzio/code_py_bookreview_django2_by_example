from django.http import HttpResponseBadRequest


def ajax_required(fn):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest  # 400
        return fn(request, *args, **kwargs)

    wrap.__doc__ = fn.__doc__
    wrap.__name__ = fn.__name__
    return wrap
