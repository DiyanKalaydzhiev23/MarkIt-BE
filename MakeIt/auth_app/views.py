from django.contrib.auth import get_user_model, authenticate, login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from auth_app.serializers import UserSerializer

UserModel = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)

        user = UserModel.objects.get(username=serializer.data['username'])

        return Response(
            {
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class LoginUserView(views.APIView):

    queryset = UserModel.objects.all()
    permission_classes = []

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'password',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
        )
    ])
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        check_user = UserModel.objects.filter(username=username)

        if not check_user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=request.user)

            data = {
                'token': token.key,
                'user_id': request.user.pk,
                'username': request.user.username,
            }

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)