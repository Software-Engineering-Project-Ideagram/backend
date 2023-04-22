from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from ideagram.api.mixins import ApiAuthMixin, ActiveProfileMixin
from ideagram.common.serializers import UUIDRelatedField
from ideagram.common.utils import inline_serializer, inline_model_serializer
from ideagram.ideas.models import Classification, Idea
from ideagram.ideas.selectors import get_all_classifications
from ideagram.ideas.services import create_idea
from ideagram.profiles.selectors import get_user_profile


class ClassificationAPI(APIView):

    class OutputClassificationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Classification
            fields = ['uuid', 'title']

    @extend_schema(responses=OutputClassificationSerializer, tags=['Classification'])
    def get(self, request):
        classifications = get_all_classifications()
        serializer = self.OutputClassificationSerializer(instance=classifications, many=True)
        return Response(data=serializer.data)




class IdeaCreateAPI(ActiveProfileMixin, APIView):
    class InputIdeaCreateSerializer(serializers.ModelSerializer):
        classification = UUIDRelatedField(queryset=Classification.objects.all(), uuid_field='uuid', many=True)
        class Meta:
            model = Idea
            fields = ['classification', 'title', 'goal', 'abstract', 'description', 'image', 'max_donation',
                      'show_likes', 'show_views', 'show_comments']

    class OutputIdeaCreateSerializer(serializers.ModelSerializer):
        classification = UUIDRelatedField(queryset=Classification.objects.all(), uuid_field='uuid', many=True)
        class Meta:
            model = Idea
            fields = ['uuid', 'classification', 'title', 'goal', 'abstract', 'description', 'image', 'max_donation',
                      'show_likes', 'show_views', 'show_comments']


    @extend_schema(request=InputIdeaCreateSerializer, tags=['Idea'])
    def post(self, request):
        serializer = self.InputIdeaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = get_user_profile(user=request.user)
        idea = create_idea(profile=profile, data=serializer.validated_data)
        output_serializer = self.OutputIdeaCreateSerializer(instance=idea)
        return Response(data=output_serializer.data)

