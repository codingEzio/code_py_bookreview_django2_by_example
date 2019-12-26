from django import forms


class CouponApplyForm(forms.Form):
    coupon_code = forms.CharField()
