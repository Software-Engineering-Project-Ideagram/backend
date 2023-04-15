from django.db import transaction

from ideagram.ideas.models import Idea
from ideagram.profiles.models import Profile


@transaction.atomic
def create_idea(*, profile: Profile, data: dict):
    classification = data.pop('classification')
    idea = Idea.objects.create(profile=profile, **data)
    idea.classification.set(classification)
    return idea


