from django.db.models import QuerySet

from ideagram.ideas.models import Classification, Idea
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
