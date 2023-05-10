from django.db import transaction
from django.db import IntegrityError

from ideagram.common.utils import update_model_instance
from ideagram.ideas.models import Idea, EvolutionStep, FinancialStep, IdeaComment, CollaborationRequest

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
def create_evolution_step(*, idea: Idea, evolution_data: dict) -> EvolutionStep | None:
    try:
        step = EvolutionStep.objects.create(idea=idea, **evolution_data)
    except IntegrityError:
        return None

    return step


@transaction.atomic
def update_evolutionary_step(*, evolutionary_step: EvolutionStep, data: dict) -> EvolutionStep:
    updated_step = update_model_instance(instance=evolutionary_step, data=data)
    return updated_step


@transaction.atomic
def create_financial_step(*, idea: Idea, financial_data: dict) -> FinancialStep | None:
    try:
        step = FinancialStep.objects.create(idea=idea, **financial_data)
    except IntegrityError:
        return None

    return step


@transaction.atomic
def update_financial_step(*, financial_step: FinancialStep, data: dict) -> FinancialStep:
    updated_step = update_model_instance(instance=financial_step, data=data)
    return updated_step


  
@transaction.atomic
def create_comment_for_idea(*, idea: Idea, profile: Profile, data: dict) -> IdeaComment:
    comment = IdeaComment.objects.create(idea=idea, profile=profile, **data)
    return comment

  
def create_collaboration_request(*, idea: Idea, data: dict) -> CollaborationRequest:
    return CollaborationRequest.objects.create(idea=idea, **data)


def update_collaboration_request(*, collaboration_request: CollaborationRequest, data: dict) -> CollaborationRequest:
    updated_request = update_model_instance(instance=collaboration_request, data=data)
    return updated_request

