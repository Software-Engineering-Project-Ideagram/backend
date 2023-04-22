from django.db import transaction

from ideagram.common.utils import update_model_instance
from ideagram.ideas.models import Idea
from ideagram.profiles.models import Profile


@transaction.atomic
def create_idea(*, profile: Profile, data: dict):
    classification = data.pop('classification')
    idea = Idea.objects.create(profile=profile, **data)
    idea.classification.set(classification)
    return idea


@transaction.atomic
def update_idea(*, idea: Idea, data: dict) -> Idea:
    updated_idea = update_model_instance(instance=idea, data=data)
    return updated_idea


