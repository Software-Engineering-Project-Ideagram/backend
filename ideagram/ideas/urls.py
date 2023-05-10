from django.urls import path

from ideagram.ideas.apis import ClassificationAPI, IdeaCreateAPI, IdeaDetailView, IdeaEvolutionStepApi, \
    IdeaEvolutionDetail, IdeaFinancialStepApi, IdeaFinancialDetail, IdeaCommentApi, IdeaCollaborationRequestApi, \
    IdeaCollaborationRequestDetailApi


urlpatterns = [
    path('classification/list', ClassificationAPI.as_view(), name="classification-list"),
    path('create', IdeaCreateAPI.as_view(), name="idea-create"),
    path('detail/<str:idea_uuid>', IdeaDetailView.as_view(), name='idea-detail'),
    path('evolution/<str:idea_uuid>', IdeaEvolutionStepApi.as_view(), name='idea-evolution'),
    path('evolution/detail/<str:evolution_uuid>', IdeaEvolutionDetail.as_view(), name='evolution-detail'),
    path('financial/<str:idea_uuid>', IdeaFinancialStepApi.as_view(), name='idea-financial'),
    path('financial/detail/<str:financial_uuid>', IdeaFinancialDetail.as_view(), name='financial-detail'),
    path('comment/<str:idea_uuid>', IdeaCommentApi.as_view(), name='idea-comment'),
    path('financial/detail/<str:financial_uuid>', IdeaFinancialDetailApi.as_view(), name='financial-detail'),
    path('collaboration/<str:idea_uuid>', IdeaCollaborationRequestApi.as_view(), name='idea-collaboration request'),
    path('collaboration/detail/<str:collaboration_uuid>', IdeaCollaborationRequestDetailApi.as_view(),
         name='collaboration-request-detail'),
]
