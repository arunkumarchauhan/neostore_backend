
from dataclasses import field
from xml.dom import ValidationErr
from django import forms
from .models import User


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['is_active']

        # def clean(self):
        #     super(UserRegisterForm, self).clean()
        #     print("Cleaned CALLED")
        #     if self.cleaned_data.get("password", None) != self.cleaned_data.get("confirm_password", ""):
        #         raise forms.ValidationError(
        #             "Password and Confirm Passwords are not same")

        def clean_password(self):
            if self.instance.password != self.instance.confirm_password:
                raise forms.ValidationError(
                    "Password and Confirm Passwords are not same")


class LoginForm(forms.Form):
    password = forms.CharField(required=True,)
    email = forms.EmailField(required=True)


class ForgotForm(forms.Form):
    email = forms.EmailField(required=True)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)


class UpdateAccountForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    phone_no = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["dob", "profile_pic"]
