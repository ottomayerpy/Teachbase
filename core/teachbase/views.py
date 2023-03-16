from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core import settings
from teachbase.client import TeachbaseClient
from teachbase.models import Course, CustomUser
from teachbase.serializers import CourseSerializer, UserCreateSerializer


class CreateUserView(CreateAPIView, ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(
        operation_summary="Invite users to account",
		    request_body=openapi.Schema(
				    type=openapi.TYPE_OBJECT,
				    properties={
					    'email':  openapi.Schema(type=openapi.TYPE_STRING, format='email'),
					    'password': openapi.Schema(type=openapi.TYPE_STRING),
					    'phone':   openapi.Schema(type=openapi.TYPE_INTEGER),
					    'external_id': openapi.Schema(type=openapi.TYPE_STRING)
				    },
				    required=['password', 'email', 'phone']
		    )
    )
    def post(self, request, *args, **kwargs):
        client = TeachbaseClient(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            base_url=settings.BASE_URL,
        )
        data = request.data
        user = client.create_user(json=data)
        user_data = self.serializer_class(data=user, many=True)
        user_data.is_valid(raise_exception=True)
        user_data.save()
        return Response(user_data.data)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CoursesListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        courses = Course.objects.all()
        if courses:
            courses_data = self.serializer_class(courses, many=True)
            return Response(courses_data.data)
        else:
            client = TeachbaseClient(
                client_id=settings.CLIENT_ID,
                client_secret=settings.CLIENT_SECRET,
                base_url=settings.BASE_URL,
            )
            courses = client.get_courses_list()
            courses_data = self.serializer_class(data=courses, many=True)
            courses_data.is_valid(raise_exception=True)
            courses_data.save()
            return Response(courses_data.data)


class CoursesDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SessionsListView(APIView):
    def get(self, response, pk):
        client = TeachbaseClient(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            base_url=settings.BASE_URL,
        )

        sessions = client.get_courses_sessions_list(course_pk=pk)
        return Response(sessions)


class SessionsUserRegister(APIView):
    @swagger_auto_schema(
        operation_summary="Register user to course session",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "phone": openapi.Schema(type=openapi.TYPE_INTEGER),
                "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    def post(self, request, pk: int):
        client = TeachbaseClient(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            base_url=settings.BASE_URL,
        )
        data = request.data

        result = client.register_user_for_session(json=data, session_pk=pk)
        return Response(result)
