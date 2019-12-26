from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import CouponApplyForm


def coupon_apply(request):
    """
    Actually, what we're doing here is only a small fraction of it.
      We simply "find" the coupon code (as a model instance which can
      be interacted with other code). For more please see the comments
      inside the 'cart/views.py :: cart_detail' (VERY thorough XD).
    """

    now = timezone.now()
    coupon_apply_form = CouponApplyForm(request.POST)
    if coupon_apply_form.is_valid():
        coupon_code = coupon_apply_form.cleaned_data["coupon_code"]
        try:
            coupon_table_inst = Coupon.objects.get(
                coupon_code__iexact=coupon_code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            request.session["coupon_id"] = coupon_table_inst.id
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None

    return redirect(to="cart:cart_detail")
