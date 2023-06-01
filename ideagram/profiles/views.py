from django.views.decorators.cache import never_cache
from django.core.cache import cache
from django.http import HttpResponse
from ideagram.users.models import BaseUser


@never_cache
def verify_email(request, token):
    email_verify = cache.get(f"email_verification_token__{token}")
    if email_verify:
        user = BaseUser.objects.get(email=email_verify)
        user.is_email_verified = True
        user.save()
        cache.delete(f"email_verification_token__{token}")
        cache.delete(f"email_verification__{email_verify}")
        return HttpResponse("Your email has been successfully verified")

    return HttpResponse("Invalid verification URL!")
