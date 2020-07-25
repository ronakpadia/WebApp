from django import forms
from django.contrib.auth.models import User
from django.core import validators
from MyApp.models import UserProfileInfo,Product, Order



class FormNewUser(forms.ModelForm):
    confirm_pass = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = User
        fields = ('username','email','password', 'confirm_pass')
    # def clean(self):
    #     super(RegistrationForm, self).clean()
    #     # This method will set the `cleaned_data` attribute
    #     password = self.cleaned_data.get('password')
    #     confirm_pass = self.cleaned_data.get('confirm_pass')
    #     if not password == confirm_pass:
    #         raise ValidationError('Passwords must match')

class FormEditProfile(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name','last_name','email')

class FormUserProfileInfo(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('somaiya_id','profile_pic')

class FormAddProduct(forms.ModelForm):
    class Meta():
        model = Product
        fields = ('product_image','product_name','product_cost')
    # def clean(self):
    #     super_cleaned = super().clean()
    #     pwd = super_cleaned.get("password")
    #     cpwd = super_cleaned.get("confirm_pass")
    #     if pwd != cpwd:
    #         raise forms.ValidationError("Passwords do not match!")
    #     else:
    #         user = User.objects.get_or_create(userid=super_cleaned.get('Somaiya_id'), password=pwd)


class FormLogin(forms.Form):
    Somaiya_id = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        super_cleaned = super().clean()
        id = super_cleaned.get("Somaiya_id")
        pwd = super_cleaned.get("password")


class FormEditOrder(forms.ModelForm):
    class Meta():
        model = Order
        fields = ('orderState',)
        labels = {
        "orderState": "Order Ready"
        }
