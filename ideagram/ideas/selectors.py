from django.db.models import QuerySet, Sum

from ideagram.ideas.models import Classification, Idea, EvolutionStep, FinancialStep, IdeaComment, CollaborationRequest, \
    IdeaAttachmentFile, IdeaLikes, OfficialInformation, SavedIdea, Donation
from ideagram.profiles.models import Profile
from ideagram.profiles.selectors import get_user_profile


from ideagram.users.models import BaseUser


def get_all_classifications() -> QuerySet(Classification):
    return Classification.objects.all()


def get_idea_by_uuid(*, uuid: str, user: BaseUser = None) -> Idea | None:
    if user:
        idea = Idea.objects.filter(uuid=uuid, profile__user=user)
    else:
        idea = Idea.objects.filter(uuid=uuid)

    if idea.exists():
        return idea.first()
    else:
        return None


def get_idea_evolutionary_steps(*, idea: Idea) -> QuerySet(EvolutionStep):
    steps = EvolutionStep.objects.filter(idea=idea)

    return steps


def get_evolutionary_step_by_uuid(*, uuid: str, user: BaseUser = None) -> EvolutionStep | None:
    if user:
        step = EvolutionStep.objects.filter(uuid=uuid, idea__profile__user=user)
    else:
        step = EvolutionStep.objects.filter(uuid=uuid)

    if step.exists():
        return step.first()
    else:
        return None


def get_idea_financial_steps(*, idea: Idea) -> QuerySet(FinancialStep):
    steps = FinancialStep.objects.filter(idea=idea)
    return steps


def get_financial_step_by_uuid(*, uuid: str, user: BaseUser = None) -> FinancialStep | None:
    if user:
        step = FinancialStep.objects.filter(uuid=uuid, idea__profile__user=user)
    else:
        step = FinancialStep.objects.filter(uuid=uuid)

    if step.exists():
        return step.first()
    else:
        return None


def get_idea_likes(*, idea_uuid: str, user: BaseUser):
    entries = IdeaLikes.objects.filter(profile_id=user.id, idea_id=idea_uuid)
    if entries.exists():
        return entries
    else:
        return None


def get_ideas_comment(*, idea: Idea) -> QuerySet(IdeaComment):
    comments = IdeaComment.objects.filter(idea=idea)
    return comments


def get_idea_collaboration_request(*, idea: Idea) -> QuerySet(CollaborationRequest):
    return CollaborationRequest.objects.filter(idea=idea)


def get_collaboration_request_by_uuid(*, uuid: str, user: BaseUser = None) -> CollaborationRequest | None:
    if user:
        request = CollaborationRequest.objects.filter(uuid=uuid, idea__profile__user=user)
    else:
        request = CollaborationRequest.objects.filter(uuid=uuid)

    if request.exists():
        return request.first()
    else:
        return None


def get_idea_attachments(*, idea: Idea) -> QuerySet(IdeaAttachmentFile):
    return IdeaAttachmentFile.objects.filter(idea=idea)


def get_attachment_by_uuid(*, uuid: str, user: BaseUser = None) -> IdeaAttachmentFile | None:
    if user:
        file = IdeaAttachmentFile.objects.filter(uuid=uuid, idea__profile__user=user)
    else:
        file = IdeaAttachmentFile.objects.filter(uuid=uuid)

    if file.exists():
        return file.first()
    else:
        return None



def get_sum_donation(*, idea: Idea):
    return Donation.objects.filter(idea=idea).aggregate(Sum('amount'))['amount__sum']


def get_idea_by_id(*, idea_id: int):
    return Idea.objects.get(id=idea_id)



def filter_ideas(
        classification: list = None, usernames: list=None, emails: list=None, sort_by: str='created_at'
        ) -> QuerySet(Idea):

    search_params = {"profile__is_public": True}

    if classification:
        search_params["classification__in"] = classification

    if usernames:
        search_params["profile__username__in"] = usernames

    if emails:
        search_params["profile__user__email__in"] = emails


    return Idea.objects.filter(**search_params).order_by(f"-{sort_by}")



def user_filter_ideas(
        profile: Profile, classification: list = None, sort_by: str='created_at'
        ) -> QuerySet(Idea):

    search_params = {"profile": profile}

    if classification:
        search_params["classification__in"] = classification


    return Idea.objects.filter(**search_params).order_by(f"-{sort_by}")


def get_official_information(*, idea: Idea) -> QuerySet(OfficialInformation):
    info = OfficialInformation.objects.filter(idea=idea)
    return info


def get_official_information_by_uuid(*, uuid: str, user: BaseUser = None) -> OfficialInformation | None:
    if user:
        info = OfficialInformation.objects.filter(uuid=uuid, idea__profile__user=user)
    else:
        info = OfficialInformation.objects.filter(uuid=uuid)

    if info.exists():
        return info.first()
    else:
        return None


def get_profile_saved_idea(*, profile: Profile) -> SavedIdea:
    return SavedIdea.objects.filter(profile=profile)


