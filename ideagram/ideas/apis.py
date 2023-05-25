from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from config.settings.idea import MAX_EVOLUTIONARY_STEPS_COUNT, MAX_FINANCIAL_STEPS_COUNT
from ideagram.api.mixins import ApiAuthMixin, ActiveProfileMixin
from ideagram.common.serializers import UUIDRelatedField
from ideagram.common.utils import inline_serializer, inline_model_serializer
from ideagram.ideas.models import Classification, Idea, EvolutionStep, FinancialStep, Organization
from ideagram.ideas.selectors import get_all_classifications, get_idea_by_uuid, get_idea_evolutionary_steps, \
    get_evolutionary_step_by_uuid, get_idea_financial_steps, get_financial_step_by_uuid
from ideagram.ideas.services import create_idea, update_idea, create_evolution_step, update_evolutionary_step, \
    create_financial_step, update_financial_step
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


class IdeaFinancialDetail(ActiveProfileMixin, APIView):
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

class OrganizationListAPI(APIView):
    class OutputOrganizationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organization
            fields = ["uuid", "name"]

    @extend_schema(responses=OutputOrganizationSerializer(many=True), tags=["Organization"])
    def get(self, request):
        organizations = Organization.objects.all()
        serializer = self.OutputOrganizationSerializer(instance=organizations, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)