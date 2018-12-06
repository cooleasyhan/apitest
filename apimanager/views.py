

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from .models import Project, RestApiTestCase
from .services import run_test


class TestSerializer(serializers.Serializer):
    project = serializers.CharField(
        allow_blank=False, max_length=120, required=True)
    api = serializers.CharField(max_length=120, required=False)


class APITestView(APIView):
    def post(self, request, format=None):
        test = TestSerializer(data=request.data)
        test.is_valid(raise_exception=True)

        try:
            project = Project.objects.get(
                name=test.validated_data['project'])
        except Project.DoesNotExist:
            raise ValidationError(detail={'project': 'Project Not Found'})
        if 'api' in test.validated_data:
            tests = RestApiTestCase.objects.filter(
                project=project, name=test.validated_data['api'])
        else:
            tests = RestApiTestCase.objects.filter(project=project)

        if len(tests) == 0:
            raise ValidationError(detail='Api Not Found')

        rst = run_test(tests)
        return Response(rst)


class AuthView(APIView):
    def post(self, request, format=None):
        return Response({"status": "ok"})
