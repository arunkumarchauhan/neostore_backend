
from django import forms


class ChangeProductQuantityForm(forms.Form):
    cart_item_id = forms.IntegerField(required=True, min_value=0)
    quantity = forms.IntegerField(required=True, min_value=0)


class AddCartItemForm(forms.Form):
    product_id = forms.IntegerField(required=True)
    quantity = forms.IntegerField(required=True)
