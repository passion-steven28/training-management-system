from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Common class for all fields
        common_classes = 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = common_classes

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "user_type",
            "first_name",
            "last_name",
            "phone",
            "organization",
            "password1",
            "password2"
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone",
            "organization",
            "profile_picture",
            "bio",
        )
