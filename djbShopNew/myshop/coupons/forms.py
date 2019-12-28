from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    coupon_code = forms.CharField(label=_("CouponCode"))
