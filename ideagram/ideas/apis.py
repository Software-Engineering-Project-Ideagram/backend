from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from ideagram.api.mixins import ApiAuthMixin, ActiveProfileMixin
from ideagram.common.serializers import UUIDRelatedField
from ideagram.common.utils import inline_serializer, inline_model_serializer
from ideagram.ideas.models import Classification, Idea
from ideagram.ideas.selectors import get_all_classifications, get_idea_by_uuid
from ideagram.ideas.services import create_idea, update_idea
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
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class IdeaDetailView(ApiAuthMixin, APIView):
    class OutputDetailSerializer(serializers.ModelSerializer):
        classification = UUIDRelatedField(queryset=Classification.objects.all(), uuid_field='uuid', many=True)

        class Meta:
            model = Idea
            fields = ['uuid', 'classification', 'title', 'goal', 'abstract', 'description', 'image', 'max_donation',
                      'show_likes', 'show_views', 'show_comments']

    class InputUpdateIdeaSerializer(serializers.ModelSerializer):
        classification = UUIDRelatedField(queryset=Classification.objects.all(), uuid_field='uuid', many=True)

        class Meta:
            model = Idea
            required_fields = []
            optional_fields = ['classification', 'title', 'goal', 'abstract', 'description', 'image', 'max_donation',
                               'show_likes', 'show_views', 'show_comments']

            fields = [*required_fields, *optional_fields]
            extra_kwargs = dict((x, {'required': False}) for x in optional_fields)

    @extend_schema(responses=OutputDetailSerializer, tags=['Idea'])
    def get(self, request, idea_uuid):
        idea = get_idea_by_uuid(uuid=idea_uuid)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)
        serializer = self.OutputDetailSerializer(instance=idea)
        return Response(data=serializer.data)


    @extend_schema(request=InputUpdateIdeaSerializer, responses=OutputDetailSerializer, tags=['Idea'])
    def put(self, request, idea_uuid):
        serializer = self.InputUpdateIdeaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        idea = get_idea_by_uuid(uuid=idea_uuid, user=request.user)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        updated_idea = update_idea(idea=idea, data=serializer.validated_data)
        serializer = self.OutputDetailSerializer(instance=updated_idea)
        return Response(data=serializer.data)

    @extend_schema(tags=['Idea'])
    def delete(self, request, idea_uuid):

        idea = get_idea_by_uuid(uuid=idea_uuid, user=request.user)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        idea.delete()
        return Response(status=status.HTTP_200_OK)
