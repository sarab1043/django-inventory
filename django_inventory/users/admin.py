from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserManager
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from . models import CustomUser, UserAddress

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation',widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        print(password1)
        password2 = self.cleaned_data.get("password2")
        print(password2)
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password dont't match")

        return password2

    def save(self,commit = True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model=CustomUser
        fields = ('email','password','first_name','last_name','is_staff','is_active','is_superuser')

class CustomUserAdmin(BaseUserManager):
    form=UserChangeForm
    add_form = UserCreationForm
    list_display=('email','first_name','last_name')
    list_filter = ('is_superuser','is_staff','is_active',)
    fieldsets = (
        (None,{'fields':('email','password')}),
        ('personal info',{'fields':('first_name','last_name')}),
        ('Permissions',{'fields':('is_superuser','is_staff','is_active')})
    )

    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('email','first_name','last_name','password1','password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(UserAddress)
