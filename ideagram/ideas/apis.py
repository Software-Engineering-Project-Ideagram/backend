from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.idea import MAX_EVOLUTIONARY_STEPS_COUNT, MAX_FINANCIAL_STEPS_COUNT
from ideagram.api.mixins import ApiAuthMixin, ActiveProfileMixin
from ideagram.common.serializers import UUIDRelatedField
from ideagram.common.utils import inline_serializer, inline_model_serializer
from ideagram.ideas.models import Classification, Idea, EvolutionStep, FinancialStep, IdeaLikes, CollaborationRequest, IdeaComment, \
    IdeaAttachmentFile

from ideagram.ideas.selectors import get_all_classifications, get_idea_by_uuid, get_idea_evolutionary_steps, \
    get_evolutionary_step_by_uuid, get_idea_financial_steps, get_financial_step_by_uuid, get_idea_likes, get_ideas_comment, \
get_idea_attachments, get_attachment_by_uuid


from ideagram.ideas.services import create_idea, update_idea, create_evolution_step, update_evolutionary_step, \
    create_financial_step, update_financial_step, like_idea, unlike_idea, create_collaboration_request, update_collaboration_request, \
    create_comment_for_idea, add_attachment_file

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
                      'show_likes', 'show_views', 'show_comments', 'views_count', 'likes_count', 'comments_count']

    class InputUpdateIdeaSerializer(serializers.ModelSerializer):
        classification = UUIDRelatedField(
            queryset=Classification.objects.all(),
            uuid_field='uuid',
            many=True,
            required=False
        )

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


class IdeaEvolutionStepApi(ActiveProfileMixin, APIView):
    class InputCreateEvolutionStepSerializer(serializers.ModelSerializer):
        priority = serializers.IntegerField(max_value=MAX_EVOLUTIONARY_STEPS_COUNT)

        class Meta:
            model = EvolutionStep
            fields = ['title', 'finish_date', 'description', 'priority']

    class OutputCreateEvolutionStepSerializer(serializers.ModelSerializer):
        idea = UUIDRelatedField(queryset=Idea.objects.all(), uuid_field='uuid')

        class Meta:
            model = EvolutionStep
            fields = ['uuid', 'idea', 'title', 'finish_date', 'description', 'priority']

    @extend_schema(responses=OutputCreateEvolutionStepSerializer, tags=['Evolution Step'])
    def get(self, request, idea_uuid):
        idea = get_idea_by_uuid(uuid=idea_uuid)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        steps = get_idea_evolutionary_steps(idea=idea)
        serializer = self.OutputCreateEvolutionStepSerializer(instance=steps, many=True)
        return Response(data=serializer.data)

    @extend_schema(request=InputCreateEvolutionStepSerializer(many=True),
                   responses=OutputCreateEvolutionStepSerializer(many=True),
                   tags=['Evolution Step'])
    def post(self, request, idea_uuid):
        idea = get_idea_by_uuid(uuid=idea_uuid, user=request.user)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        serializer = self.InputCreateEvolutionStepSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        created_steps = []

        for data in serializer.validated_data:
            step = create_evolution_step(idea=idea, evolution_data=data)
            if step:
                created_steps.append(step)
            else:
                return Response(f"invalid priority: {data['priority']}", status=status.HTTP_400_BAD_REQUEST)

        output_serializer = self.OutputCreateEvolutionStepSerializer(instance=created_steps, many=True)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class IdeaEvolutionDetail(ActiveProfileMixin, APIView):
    class InputUpdateEvolutionStepSerializer(serializers.ModelSerializer):
        class Meta:
            model = EvolutionStep
            optional_fields = ['title', 'finish_date', 'description']
            required_fields = []
            fields = [*optional_fields, *required_fields]
            extra_kwargs = dict((x, {'required': False}) for x in optional_fields)

    class OutputEvolutionStepDetailSerializer(serializers.ModelSerializer):
        idea = UUIDRelatedField(queryset=Idea.objects.all(), uuid_field='uuid')

        class Meta:
            model = EvolutionStep
            fields = ['uuid', 'idea', 'title', 'finish_date', 'description', 'priority']

    @extend_schema(request=InputUpdateEvolutionStepSerializer,
                   responses=OutputEvolutionStepDetailSerializer,
                   tags=['Evolution Step'])
    def put(self, request, evolution_uuid):
        serializer = self.InputUpdateEvolutionStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        step = get_evolutionary_step_by_uuid(uuid=evolution_uuid, user=request.user)
        if not step:
            return Response("No evolutionary step found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        updated_step = update_evolutionary_step(evolutionary_step=step, data=serializer.validated_data)
        output_serializer = self.OutputEvolutionStepDetailSerializer(instance=updated_step)
        return Response(data=output_serializer.data)

    @extend_schema(tags=['Evolution Step'])
    def delete(self, request, evolution_uuid):

        step = get_evolutionary_step_by_uuid(uuid=evolution_uuid, user=request.user)
        if not step:
            return Response("No evolutionary step with this uuid!", status=status.HTTP_404_NOT_FOUND)

        step.delete()
        return Response(status=status.HTTP_200_OK)


# ===============================================================================================

class IdeaFinancialStepApi(ActiveProfileMixin, APIView):
    class InputCreateFinancialStepSerializer(serializers.ModelSerializer):
        priority = serializers.IntegerField(max_value=MAX_FINANCIAL_STEPS_COUNT)

        class Meta:
            model = FinancialStep
            fields = ['title', 'cost', 'description', 'priority', 'unit']

    class OutputCreateFinancialStepSerializer(serializers.ModelSerializer):
        idea = UUIDRelatedField(queryset=Idea.objects.all(), uuid_field='uuid')

        class Meta:
            model = FinancialStep
            fields = ['uuid', 'idea', 'title', 'cost', 'description', 'priority', 'unit']

    @extend_schema(responses=OutputCreateFinancialStepSerializer, tags=['Financial Step'])
    def get(self, request, idea_uuid):
        idea = get_idea_by_uuid(uuid=idea_uuid)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        steps = get_idea_financial_steps(idea=idea)
        serializer = self.OutputCreateFinancialStepSerializer(instance=steps, many=True)
        return Response(data=serializer.data)

    @extend_schema(request=InputCreateFinancialStepSerializer(many=True),
                   responses=OutputCreateFinancialStepSerializer(many=True),
                   tags=['Financial Step'])
    def post(self, request, idea_uuid):
        idea = get_idea_by_uuid(uuid=idea_uuid, user=request.user)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        serializer = self.InputCreateFinancialStepSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        created_steps = []

        for data in serializer.validated_data:
            step = create_financial_step(idea=idea, financial_data=data)
            if step:
                created_steps.append(step)
            else:
                return Response(f"invalid priority: {data['priority']}", status=status.HTTP_400_BAD_REQUEST)

        output_serializer = self.OutputCreateFinancialStepSerializer(instance=created_steps, many=True)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class IdeaFinancialDetailApi(ActiveProfileMixin, APIView):
    class InputUpdateFinancialStepSerializer(serializers.ModelSerializer):
        class Meta:
            model = FinancialStep
            optional_fields = ['title', 'cost', 'description', 'unit']
            required_fields = []
            fields = [*optional_fields, *required_fields]
            extra_kwargs = dict((x, {'required': False}) for x in optional_fields)

    class OutputFinancialStepDetailSerializer(serializers.ModelSerializer):
        idea = UUIDRelatedField(queryset=Idea.objects.all(), uuid_field='uuid')

        class Meta:
            model = FinancialStep
            fields = ['uuid', 'idea', 'title', 'cost', 'description', 'priority', 'unit']

    @extend_schema(request=InputUpdateFinancialStepSerializer,
                   responses=OutputFinancialStepDetailSerializer,
                   tags=['Financial Step'])
    def put(self, request, financial_uuid):
        serializer = self.InputUpdateFinancialStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        step = get_financial_step_by_uuid(uuid=financial_uuid, user=request.user)
        if not step:
            return Response("No financial step found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        updated_step = update_financial_step(financial_step=step, data=serializer.validated_data)
        output_serializer = self.OutputFinancialStepDetailSerializer(instance=updated_step)
        return Response(data=output_serializer.data)

    @extend_schema(tags=['Financial Step'])
    def delete(self, request, financial_uuid):

        step = get_financial_step_by_uuid(uuid=financial_uuid, user=request.user)
        if not step:
            return Response("No financial step with this uuid!", status=status.HTTP_404_NOT_FOUND)

        step.delete()
        return Response(status=status.HTTP_200_OK)



class IdeaLikeApi(APIView):

    class UserLikeSerializer(serializers.ModelSerializer):
        class Meta:
            model = IdeaLikes
            fields = ['profile_id']

    @extend_schema(responses=UserLikeSerializer(many=True), tags=['Idea Like'])
    def get(self, request, idea_uuid):
        try:
            queryset = get_idea_likes(idea_uuid=idea_uuid, user=request.user)
            serializer = self.UserLikeSerializer(queryset, many=True)
            return Response(serializer.data)
        except Idea.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(tags=['Idea Like'])
    def post(self, request, idea_uuid):
        temp = like_idea(idea_uuid=idea_uuid, user_id=request.user.id)
        if temp is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(tags=['Idea Like'])
    def delete(self, request, idea_uuid):
        unlike_idea(idea_uuid=idea_uuid, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

      
class IdeaCommentApi(ActiveProfileMixin, APIView):
    class InputIdeaCommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = IdeaComment
            fields = ["comment"]

    class OutputIdeaCommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = IdeaComment
            fields = ["uuid", "date", "profile", "idea", 'comment']

    @extend_schema(responses=OutputIdeaCommentSerializer(many=True), tags=["Comments"])
    def get(self, request, idea_uuid):
        idea = get_idea_by_uuid(uuid=idea_uuid)
        if not idea.show_comments:
            return Response(data={'message': "Idea's comments are hidden"}, status=status.HTTP_403_FORBIDDEN)

        comments = get_ideas_comment(idea=idea)
        serializer = self.OutputIdeaCommentSerializer(instance=comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=InputIdeaCommentSerializer, responses=OutputIdeaCommentSerializer, tags=["Comments"])
    def post(self, request, idea_uuid):
        serializer = self.InputIdeaCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        idea = get_idea_by_uuid(uuid=idea_uuid)
        profile = get_user_profile(user=request.user)
        comment = create_comment_for_idea(idea=idea, profile=profile, data=serializer.validated_data)
        output_serializer = self.OutputIdeaCommentSerializer(instance=comment)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)

      
class IdeaCollaborationRequestApi(ActiveProfileMixin, APIView):
    class InputIdeaCollaborationRequestSerializer(serializers.ModelSerializer):

        class Meta:
            model = CollaborationRequest
            fields = ['skills', 'age', 'education', 'description', 'salary']

    class OutputCollaborationRequestSerializer(serializers.ModelSerializer):
        idea = UUIDRelatedField(queryset=Idea.objects.all(), uuid_field='uuid')

        class Meta:
            model = CollaborationRequest
            fields = ['uuid', 'idea', 'skills', 'age', 'description', 'education', 'salary']

    @extend_schema(responses=OutputCollaborationRequestSerializer, tags=['Collaboration Request'])
    def get(self, request, idea_uuid):
        idea = get_idea_by_uuid(uuid=idea_uuid)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)
        collaboration_request = get_idea_collaboration_request(idea=idea)
        serializer = self.OutputCollaborationRequestSerializer(instance=collaboration_request, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=InputIdeaCollaborationRequestSerializer(),
                   responses=OutputCollaborationRequestSerializer(),
                   tags=['Collaboration Request'])
    def post(self, request, idea_uuid):
        idea = get_idea_by_uuid(uuid=idea_uuid, user=request.user)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        serializer = self.InputIdeaCollaborationRequestSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        new_collaboration_request = create_collaboration_request(idea=idea, data=serializer.validated_data)

        output_serializer = self.OutputCollaborationRequestSerializer(instance=new_collaboration_request)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)


class IdeaCollaborationRequestDetailApi(ActiveProfileMixin, APIView):
    class InputUpdateCollaborationRequestSerializer(serializers.ModelSerializer):
        class Meta:
            model = CollaborationRequest
            optional_fields = ['skills', 'age', 'description', 'education','salary']
            required_fields = []
            fields = [*optional_fields, *required_fields]
            extra_kwargs = dict((x, {'required': False}) for x in optional_fields)

    class OutputCollaborationRequestDetailSerializer(serializers.ModelSerializer):
        idea = UUIDRelatedField(queryset=Idea.objects.all(), uuid_field='uuid')

        class Meta:
            model = CollaborationRequest
            fields = ['uuid', 'idea', 'skills', 'age', 'description', 'education', 'salary']

    @extend_schema(request=InputUpdateCollaborationRequestSerializer,
                   responses=OutputCollaborationRequestDetailSerializer,
                   tags=['Collaboration Request'])
    def put(self, request, collaboration_request_uuid):
        serializer = self.InputUpdateCollaborationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request = get_collaboration_request_by_uuid(uuid=collaboration_request_uuid, user=request.user)
        if not request:
            return Response("No collaboration request found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        updated_request = update_collaboration_request(collaboration_request=request, data=serializer.validated_data)
        output_serializer = self.OutputCollaborationRequestDetailSerializer(instance=updated_request)
        return Response(data=output_serializer.data)

    @extend_schema(tags=['Collaboration Request'])
    def delete(self, request, collaboration_request_uuid):

        request = get_collaboration_request_by_uuid(uuid=collaboration_request_uuid, user=request.user)
        if not request:
            return Response("No collaboration request with this uuid!", status=status.HTTP_404_NOT_FOUND)

        request.delete()
        return Response(status=status.HTTP_200_OK)


class IdeaAttachmentApi(ActiveProfileMixin, APIView):
    class InputAttachmentSerializer(serializers.Serializer):
        file = serializers.FileField()

    class OutputAttachmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = IdeaAttachmentFile
            fields = ['uuid', 'file', 'created_at']


    @extend_schema(responses=OutputAttachmentSerializer(many=True), tags=["Attachments"])
    def get(self, request, idea_uuid):
        idea = get_idea_by_uuid(uuid=idea_uuid)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        attachments = get_idea_attachments(idea=idea)
        serializer = self.OutputAttachmentSerializer(instance=attachments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=InputAttachmentSerializer, responses=OutputAttachmentSerializer, tags=["Attachments"])
    def post(self, request, idea_uuid):
        serializer = self.InputAttachmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        idea = get_idea_by_uuid(uuid=idea_uuid, user=request.user)
        if not idea:
            return Response("No idea found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        attachment = add_attachment_file(idea=idea, data=serializer.validated_data)
        if not attachment:
            return Response("Maximum number of attachment reached!", status=status.HTTP_403_FORBIDDEN)

        output_serializer = self.OutputAttachmentSerializer(instance=attachment)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)



class IdeaAttachmentDetailApi(ActiveProfileMixin, APIView):

    @extend_schema(tags=["Attachments"])
    def delete(self, request, attachment_uuid):
        attachment = get_attachment_by_uuid(uuid=attachment_uuid, user=request.user)
        if not request:
            return Response("No attachment found with this uuid!", status=status.HTTP_404_NOT_FOUND)

        attachment.delete()
        return Response(status=status.HTTP_200_OK)


