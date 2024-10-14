import threading

from django.conf import settings as django_settings
from django.core import signing
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from authentication.exceptions import TokenScopeError


def get_token(user, action, **kwargs):
    username = user.get_username()
    if hasattr(username, "pk"):
        username = username.pk
    payload = {user.USERNAME_FIELD: username, "action": action}
    if kwargs:
        payload.update(**kwargs)
    token = signing.dumps(payload)
    return token


def get_token_paylod(token, action, exp=None):
    payload = signing.loads(token, max_age=exp)
    _action = payload.pop("action")
    if _action != action:
        raise TokenScopeError
    return payload


def using_refresh_tokens():
    if (
        hasattr(django_settings, "GRAPHQL_JWT")
        and django_settings.GRAPHQL_JWT.get("JWT_LONG_RUNNING_REFRESH_TOKEN", False)
        and "jwt.refresh_token.apps.RefreshTokenConfig"
        in django_settings.INSTALLED_APPS
    ):
        return True
    return False


def revoke_user_refresh_token(user):
    if using_refresh_tokens():
        refresh_tokens = user.refresh_tokens.all()
        for refresh_token in refresh_tokens:
            try:
                refresh_token.revoke()
            except Exception:  # JSONWebTokenError
                pass


def flat_dict(dict_or_list):
    """
    if is dict, return list of dict keys,
    if is list, return the list
    """
    return list(dict_or_list.keys()) if isinstance(dict_or_list, dict) else dict_or_list


def normalize_fields(dict_or_list, extra_list):
    """
    helper merge settings defined fileds and
    other fields on mutations
    """
    if isinstance(dict_or_list, dict):
        for i in extra_list:
            dict_or_list[i] = "String"
        return dict_or_list
    else:
        return dict_or_list + extra_list


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_verification_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        EmailThread(email).start()

    def send_email(data):
        subject = data['email_subject']
        html_content = render_to_string(
            'email_template.html', data['email_context'])
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject, text_content, 'from@example.com', [data['to_email']])
        email.attach_alternative(html_content, "text/html")
        email.send()
