from django.db import transaction
from django.db import IntegrityError

from config.settings.idea import MAX_FILE_ATTACHMENT_COUNT
from ideagram.common.utils import update_model_instance

from ideagram.ideas.models import Idea, EvolutionStep, FinancialStep, IdeaComment, CollaborationRequest, \
    IdeaAttachmentFile, IdeaLikes

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
def like_idea(*, idea_uuid: str, user_id: str):
    try:
        return IdeaLikes.objects.create(idea_id=idea_uuid, profile_id=user_id)
    except IntegrityError:
        return None


@transaction.atomic
def unlike_idea(*, idea_uuid: str, user):
    try:
        entry = IdeaLikes.objects.get(uuid=idea_uuid, user=user)
        entry.delete()
    except IdeaLikes.DoesNotExist:
        return None

  
@transaction.atomic
def create_comment_for_idea(*, idea: Idea, profile: Profile, data: dict) -> IdeaComment:
    comment = IdeaComment.objects.create(idea=idea, profile=profile, **data)
    return comment


@transaction.atomic
def create_collaboration_request(*, idea: Idea, data: dict) -> CollaborationRequest:
    return CollaborationRequest.objects.create(idea=idea, **data)


@transaction.atomic
def update_collaboration_request(*, collaboration_request: CollaborationRequest, data: dict) -> CollaborationRequest:
    updated_request = update_model_instance(instance=collaboration_request, data=data)
    return updated_request


@transaction.atomic
def add_attachment_file(*, idea: Idea, data: dict) -> IdeaAttachmentFile | None:
    if idea.attached_files_count >= MAX_FILE_ATTACHMENT_COUNT:
        return None

    attachment = IdeaAttachmentFile.objects.create(idea=idea, **data)
    idea.attached_files_count += 1
    idea.save()
    return attachment


