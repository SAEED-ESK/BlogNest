from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=250,
        required=True,
        label="نام",
        widget=forms.TextInput(
            attrs={
                "placeholder": "نام شما",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=250,
        required=True,
        label="نام خانوادگی",
        widget=forms.TextInput(
            attrs={
                "placeholder": "نام خانوادگی شما",
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "example@email.com",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            user.profile.first_name = self.cleaned_data["first_name"]
            user.profile.last_name = self.cleaned_data["last_name"]
            user.profile.save()

        return user