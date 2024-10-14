from datetime import date

import requests
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic.edit import FormView

from authentication.forms import (
    NewUserLoginForm,
    UserRegisterForm,
    UserUpdateForm,
)
from authentication.models import UserPrograms, UserSubscription
from dashboard.models import Program
from victor import settings

User = get_user_model()  # noqa: F811

# signup and email confirmation code

class SignUpView(FormView):
    template_name = "signup/signup.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("signup_done")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account till it is confirmed
        user.save()

        # Email verification
        current_site = get_current_site(self.request)
        mail_subject = "Activate your account."

        # Render HTML and plain text email content
        html_message = render_to_string(
            "signup/acc_active_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
        )
        plain_message = strip_tags(html_message)  # Convert HTML to plain text

        to_email = form.cleaned_data.get("email")

        email = EmailMultiAlternatives(
            subject=mail_subject,
            body=plain_message,
            from_email="shapentone360@gmail.com",
            to=[to_email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

        return redirect('registration_success')


def signup_success(request):
    return render(request, 'signup/signup_success.html')


def account_verified(request):
    return render(request, 'signup/account_verified.html')


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_email_verified = True
            user.save()
            login(request, user)  # Log the user in after activation

            # Prepare and send confirmation email
            current_site = get_current_site(request)
            mail_subject = 'Email Verified and Account Activated'
            html_message = render_to_string(
                "signup/acc_activated_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                }
            )
            # Convert HTML to plain text
            plain_message = strip_tags(html_message)

            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            email = EmailMultiAlternatives(
                subject=mail_subject,
                body=plain_message,
                from_email=from_email,
                to=recipient_list,
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

            return HttpResponseRedirect('/account-verified/')
        else:
            return HttpResponse("Activation link is invalid!")


def activation_failed(request):
    return render(request, 'activation_failed.html')


# class LoginRequest(View):
#     form_class = NewUserLoginForm
#     initial = {"key": "value"}
#     template_name = "signin.html"

#     def get(self, request):
#         form = self.form_class(request.POST)
#         # return render(request, self.template_name, {"form": form, 'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})
#         return render(request, self.template_name, {"form": form})

#     def post(self, request):

#         if request.user.is_authenticated:
#             return redirect("dashboard")

#         if request.method == 'POST':
#             form = NewUserLoginForm(data=request.POST)
#             # try:
#             login(request, form.get_user())
#             # except BadHeaderError:
#             #     return HttpResponse('Invalid header found.')
#             messages.success(request, "Welocome to victor Fitness")
#             return redirect('dashboard')
#         else:
#             form = NewUserLoginForm()
#             return render(request, self.template_name, {"form": form})
#             # if form.is_valid():
#             #     ''' reCAPTCHA validation '''
#             #     recaptcha_response = request.POST.get('g-recaptcha-response')
#             #     data = {
#             #         'secret': settings.RECAPTCHA_PRIVATE_KEY,
#             #         'response': recaptcha_response
#             #     }
#             #     r = requests.post(
#             #         'https://www.google.com/recaptcha/api/siteverify', data=data)
#             #     result = r.json()

#             #     print(result)
#             #     ''' if reCAPTCHA returns True '''
#             #     if result['success']:
#             #         try:
#             #             login(request, form.get_user())
#             #         except BadHeaderError:
#             #             return HttpResponse('Invalid header found.')
#             #         messages.success(request, "Welocome to victor Fitness")
#             #     # login(request, form.get_user())
#             #     # Redirect to home page after successful login
#             #     return redirect('dashboard')
#             # else:
#             #     form = NewUserLoginForm()
#             #     return render(request, self.template_name, {"form": form})
#         # else:
#         #     form = self.form_class(request.POST)

class LoginRequest(View):
    form_class = NewUserLoginForm
    template_name = "signin.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome to Victor Fitness")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name, {"form": form})
    
class SignUpRequest(View):
    form_class = UserRegisterForm
    initial = {"key": "value"}
    template_name = "signup.html"

    async def get(self, request):
        form = self.form_class(request.POST)
        return render(request, self.template_name, {"form": form, 'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})

    async def post(self, request):
        if request.method == "POST":
            next = request.GET.get("next")
            form = self.form_class(request.POST)
            if form.is_valid():
                ''' reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                data = {
                    'secret': settings.RECAPTCHA_PRIVATE_KEY,
                    'response': recaptcha_response
                }
                r = requests.post(
                    'https://www.google.com/recaptcha/api/siteverify', data=data)
                result = r.json()

                print(result)
                ''' if reCAPTCHA returns True '''
                if result['success']:
                    try:
                        user = form.save(commit=False)
                        password = form.cleaned_data.get("password")
                        user.set_password(password)
                        user.save()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, "Welocome to victor Fitness")
                # new_user = authenticate(email=user.email, password=password)
                # login(request, new_user)
                user = form.save(commit=False)
                password = form.cleaned_data.get("password")
                user.set_password(password)
                user.save()
                if next:
                    return redirect(next)
                else:
                    return redirect("verify-email")
        else:
            form = self.form_class(request.POST)
        context = {"form": form,
                   'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY}
        return render(request, self.template_name, context)


def signup_view(request):
    if request.method == "POST":
        next = request.GET.get("next")
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            # new_user = authenticate(email=user.email, password=password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # login(request, new_user)
            if next:
                return redirect(next)
            else:
                return redirect("verify-email")
    else:
        form = UserRegisterForm()
    context = {"form": form}
    return render(request, "signup.html", context)


# send email with verification link
# def verify_email(request):
#     if request.method == "POST":
#         if request.user.is_email_verified != True:
#             current_site = get_current_site(request)
#             user = request.user
#             email = request.user.email
#             subject = "Verify Email"
#             message = render_to_string(
#                 "verify_email_message.html",
#                 {
#                     "request": request,
#                     "user": user,
#                     "domain": current_site.domain,
#                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                     "token": account_activation_token.make_token(user),
#                 },
#             )
#             email = EmailMessage(subject, message, to=[email])
#             email.content_subtype = "html"
#             email.send()
#             return redirect("verify-email-done")
#         else:
#             return redirect("signup")
#     return render(request, "verify_email.html")


# def verify_email_done(request):
#     return render(request, "verify_email_done.html")


# def verify_email_confirm(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_email_verified = True
#         user.save()
#         messages.success(request, "Your email has been verified.")
#         return redirect("verify-email-complete")
#     else:
#         messages.warning(request, "The link has expired.")
#     return render(request, "verify_email_confirm.html")


# def verify_email_complete(request):
#     return render(request, "verify_email_complete.html")


# views.py


class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    template_name = 'reset/password_reset_form.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'reset/password_reset_confirm.html'



class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'reset/password_reset_done.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'reset/password_reset_complete.html'

@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        today = date.today()  # noqa: F841
        user_form = UserUpdateForm()
        user_id = self.request.user.id
        user_subscription = UserSubscription.objects.filter(user=user_id).order_by(
            "-id"
        )[:1]
        programs = Program.objects.all()
        user_program = UserPrograms.objects.filter(active=True)

        context = {
            "update_form": user_form,
            "user_subscription": user_subscription,
            "programs": programs,
            "user_program": user_program,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if request.method == "POST":
            form = UserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()

                messages.success(request, "Your Profile has been updated!")
                return redirect("profile")
        else:
            form = UserUpdateForm()
        return render(request, 'profile.html', {"update_form": form})


@method_decorator(login_required, name="dispatch")
class UpdateProfile(View):
    def get(self, request):

        form = UserUpdateForm(instance=request.user)

        return render(request, "user_update.html", {"form": form})

    def post(self, request):
        if request.method == "POST":

            form = UserUpdateForm(data=request.POST, instance=request.user)

            if form.is_valid():

                form.save()

                messages.success(request, "Your Profile has been updated!")
                return redirect("user_settings")

        else:
            form = UserUpdateForm()
            return redirect("user_settings")


# @method_decorator(login_required, name='dispatch')
# class UpdateProfile(View):


@method_decorator(login_required, name="dispatch")
class PasswordChange(View):
    def get(self, request):
        user = request.user
        form = SetPasswordForm(user)

        context = {
            "form": form,
        }

        return render(request, "user_update.html", context)

    def post(self, request):
        if request.method == "POST":

            user = request.user
            form = SetPasswordForm(user)

            if form.is_valid():
                form.save()

            messages.success(
                request, "Your password has been Updated successfully!")
            return redirect("update-profile")
        else:
            form = UserUpdateForm()
            return redirect("update-profile")


class Intake(View):
    def get(self, request):
        return render(request, "intake.html")


@login_required
def logout_request(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")


@login_required
class InvoiceCreateView(View):
    model = UserSubscription
    fields = [
        "subscription",
        "start_date",
    ]

    def form_valid(self, form):
        # Save the form data without committing to the database
        user = self.request.user

        form.instance.user = user if user else None

        form.instance.start_date = timezone.now().date()
        invoice = form.save(commit=False)
        invoice.save()

        # Store the invoice number in the session
        self.request.session["invoice_number"] = invoice.invoice_no

        print(self.request.session["invoice_number"])

        return redirect("create_invoice")

    def get_success_url(self):
        # Retrieve the invoice number from the session
        invoice_number = self.request.session.get("invoice_number")

        # Redirect to a URL with the invoice number
        return reverse_lazy("payment", kwargs={"invoice_number": invoice_number})


@method_decorator(login_required, name='dispatch')
class CreateUserProgramView(View):
    def post(self, request):
        # Assuming you're sending program_id as POST parameter
        program_id = request.POST.get('program_id')
        active = True  # request.POST.get('active') == True
        custom = False  # request.POST.get('custom') == False

        # Fetch the Program instance based on the provided id
        try:
            program = Program.objects.get(id=program_id)
        except Program.DoesNotExist:
            messages.error(request, 'Program does not exist')
            return redirect('dashboard')
            # return JsonResponse({'error': str(e)}, status=400)

        # Check if there is an existing record with the same user and program
        existing_record = UserPrograms.objects.filter(
            Q(user=request.user) & Q(program=program)
        ).first()

        if existing_record:
            # If a record exists, you can decide to update it or return an error
            messages.error(request, 'Record already exists')
            return redirect('dashboard')
            # return JsonResponse({'error': 'A record with the same user and program already exists.'}, status=400)

        # If no existing record, create the UserPrograms instance with the logged-in user
        user_program = UserPrograms(
            user=request.user, program=program, active=active, custom=custom)
        user_program.save()

        # Return a success response
        messages.success(request, "UserProgram created successfully")
        return redirect('dashboard')
        # return JsonResponse({'success': 'UserProgram created successfully', 'id': user_program.id})


def auth(request):
    return render(request, 'auth.html')
