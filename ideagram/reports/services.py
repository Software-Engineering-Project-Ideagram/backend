from django.db import transaction

from ideagram.profiles.models import Profile
from ideagram.profiles.selectors import get_profile_using_username
from ideagram.reports.models import ProfileReport
from ideagram.users.models import BaseUser


@transaction.atomic
def create_profile_report(*, reporter:Profile, data: dict) -> ProfileReport:
    reported_profile = get_profile_using_username(username=data.pop("profile_username"))
    if not reported_profile:
        raise ValueError("profile_username doesn't exists")
    profile_report = ProfileReport.objects.create(reporter_id=reporter, profile_id=reported_profile, **data)
    return profile_report
