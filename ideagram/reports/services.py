from django.db import transaction

from config.settings.report import IDEA_MAX_REPORT_COUNT
from ideagram.ideas.selectors import get_idea_by_uuid
from ideagram.profiles.models import Profile
from ideagram.profiles.selectors import get_profile_using_username
from ideagram.reports.models import ProfileReport,IdeaReport


@transaction.atomic
def create_profile_report(*, reporter:Profile, data: dict) -> ProfileReport:
    reported_profile = get_profile_using_username(username=data.pop("profile_username"))
    if not reported_profile:
        raise ValueError("profile_username doesn't exists")
    profile_report = ProfileReport.objects.create(reporter_id=reporter, profile_id=reported_profile, **data)
    return profile_report


@transaction.atomic
def create_idea_report(*, reporter:Profile, data: dict) -> IdeaReport:
    idea = get_idea_by_uuid(uuid=data.pop("idea"))
    if not idea:
        raise ValueError("idea doesn't exists")
    idea_report = IdeaReport.objects.create(reporter=reporter, idea=idea, **data)

    reports = IdeaReport.objects.filter(idea=idea, is_checked=False)

    if reports.count() > IDEA_MAX_REPORT_COUNT:
        idea.is_active = False
        idea.save()

    return idea_report
