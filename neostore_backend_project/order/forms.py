
from django import forms


class PlaceOrderForm(forms.Form):
    address_id = forms.IntegerField(required=True, min_value=0)


class GetOrderDetailForm(forms.Form):
    order_id = forms.IntegerField(required=True, min_value=0)
