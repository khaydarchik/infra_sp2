import random
import string
from django.shortcuts import get_object_or_404

from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from api.permissions import IsAdmin
from api.serializers import (UserMeSerializer, UserSerializer,
                             UserSingSerializer, UserTokenSerializer)
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    @action(
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        methods=['get', 'patch']
    )
    def users_me(self, request):
        if request.method == 'GET':
            serializer = UserMeSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserCreate(APIView):

    def post(self, request):
        serializer = UserSingSerializer(data=request.data)
        confirmation_code = ''.join(
            random.choice(
                string.ascii_uppercase + string.digits) for x in range(6)
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(confirmation_code=confirmation_code)
        send_mail(
            'confirmation_code',
            f'Ваш код для генерации токена: {confirmation_code}',
            'from@example.com', [request.data['email']],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserToken(APIView):

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=request.data['username'])
        if request.data['confirmation_code'] == user.confirmation_code:
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
