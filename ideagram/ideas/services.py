from django.db import transaction
from django.db import IntegrityError

from ideagram.common.utils import update_model_instance
from ideagram.ideas.models import Idea, EvolutionStep
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


@transaction.atomic
def create_evolution_step(*,idea: Idea, evolution_data: dict) -> EvolutionStep | None:
    try:
        step = EvolutionStep.objects.create(idea=idea, **evolution_data)
    except IntegrityError:
        return None

    return step


@transaction.atomic
def update_evolutionary_step(*, evolutionary_step: EvolutionStep, data: dict) -> EvolutionStep:
    updated_step = update_model_instance(instance=evolutionary_step, data=data)
    return updated_step

