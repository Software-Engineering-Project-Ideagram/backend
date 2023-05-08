from django.db.models import QuerySet

from ideagram.ideas.models import Classification, Idea, EvolutionStep, FinancialStep, IdeaComment
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


def get_ideas_comment(*, idea: Idea) -> QuerySet(IdeaComment):
    comments = IdeaComment.objects.filter(idea=idea)
    return comments
