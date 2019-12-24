from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]


class CartAddProductForm(forms.Form):
    """
    Form is HTML, but the state & data was managed by Python/Django.

    Here are some rough procedures (init: initializing forms)
    1> display(view)  init, return into templates through `context` (render)
    2> display(tmpl)  init with a csrf_token, which view should process this
    3> process(view)  init, clean, redirect (doesn't have to be saved to DB!)
    4> display(tmpl)  redirected page (surely related to processing result)
    """

    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int
    )
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
