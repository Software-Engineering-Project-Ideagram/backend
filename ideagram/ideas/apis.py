from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from ideagram.ideas.models import Classification
from ideagram.ideas.selectors import get_all_classifications


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



