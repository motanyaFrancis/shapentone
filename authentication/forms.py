from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django_recaptcha.fields import ReCaptchaField, ReCaptchaV3

from victor import settings

User = get_user_model()


class NewUserLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3(action='/login/'))

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            'captcha',
        ]

        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "email@example.com", "class": "form-control"}),
            "password": forms.PasswordInput(attrs={"placeholder": "enter your passsword", "class": "form-control"}),
        }


class UserRegisterForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "password",
            'captcha',
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "john", 'required': True}),
            "last_name": forms.TextInput(attrs={"placeholder": "Doe", 'required': True}),
            "email": forms.EmailInput(attrs={"placeholder": "example@email.com"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Enter password"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "w-100", 'required': True}),
        }

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        email_check = User.objects.filter(email=email)
        dob = self.cleaned_data.get("date_of_birth")
        age = (date.today() - dob).days / 365

        if email_check.exists():
            raise forms.ValidationError("This Email already exists")

        if len(password) < 5:
            raise forms.ValidationError(
                "Your password should have more than 5 characters"
            )

        if age < 18:
            raise forms.ValidationError(
                "You must be at least 18 years old to Join")

        return super(UserRegisterForm, self).clean(*args, **kwargs)


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User

        date_of_birth = forms.DateField(
            input_formats=settings.DATE_INPUT_FORMATS)

        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "date_of_birth",
            "current_weight",
            "Target_weight",
            "height",
        ]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields["date_of_birth"].widget = forms.DateInput(
            attrs={"type": "date"})
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="col-md-4"),
                Column("middle_name", css_class="col-md-4"),
                Column("last_name", css_class="col-md-4"),
            ),
            Row(
                Column("email", css_class="col-md-12"),
                Column("date_of_birth", css_class="col-md-12"),
            ),
            Row(
                Column("current_weight", css_class="col-md-6"),
                Column("Target_weight", css_class="col-md-6"),
            ),
            Row(
                Column("height", css_class="col-md-12"),
            ),
        )

    def clean(self, *args, **kwargs):
        dob = self.cleaned_data.get("date_of_birth")
        if not dob:
            dob = date(1988, 2, 19)
        age = (date.today() - dob).days / 365

        if age < 18:
            raise forms.ValidationError(
                "Date of birth should not be lower than the age of majority(18yrs)."
            )

        return super(UserUpdateForm, self).clean(*args, **kwargs)


class Set_Password_Form(SetPasswordForm):

    class Meta:
        model = get_user_model
        fields = ["new_password1", "new_password2"]


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Enter your email", max_length=254)

    
        
