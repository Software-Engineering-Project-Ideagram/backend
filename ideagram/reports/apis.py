from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ideagram.api.mixins import ApiAuthMixin
from ideagram.profiles.selectors import get_user_profile
from ideagram.reports.models import ProfileReport
from ideagram.reports.services import create_profile_report


class ProfileReportAPI(ApiAuthMixin, APIView):
    class InputProfileReportSerializer(serializers.ModelSerializer):
        profile_username = serializers.CharField(max_length=128)

        class Meta:
            model = ProfileReport
            fields = ["profile_username", "report_reasons", "description"]

    @extend_schema(request=InputProfileReportSerializer, tags=["Reports"])
    def post(self, request):
        profile_report = self.InputProfileReportSerializer(data=request.data)
        profile_report.is_valid(raise_exception=True)
        reporter_profile = get_user_profile(user=request.user)
        try:
            create_profile_report(reporter=reporter_profile, data=profile_report.validated_data)
        except ValueError as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
