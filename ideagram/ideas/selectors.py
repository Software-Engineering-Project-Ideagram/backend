from django.db.models import QuerySet

from ideagram.ideas.models import Classification


def get_all_classifications() -> QuerySet(Classification):
    return Classification.objects.all()