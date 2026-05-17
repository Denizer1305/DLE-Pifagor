from __future__ import annotations

from apps.users.serializers import (
    AccessTokenSerializer,
    EmailVerificationSerializer,
    ForgotPasswordSerializer,
    GuardianRegistrationSerializer,
    LearnerRegistrationSerializer,
    LoginSerializer,
    MinorLearnerRegistrationSerializer,
    RefreshTokenSerializer,
    ResetPasswordSerializer,
    TeacherRegistrationSerializer,
    UserDetailSerializer,
)
from apps.users.services import (
    blacklist_refresh_token,
    clear_refresh_token_cookie,
    get_refresh_token_from_request,
    login_user,
    refresh_access_token,
    register_guardian,
    register_learner,
    register_minor_learner_by_guardian,
    register_teacher,
    request_password_reset,
    reset_password_by_token,
    set_refresh_token_cookie,
    verify_email_token,
)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    """
    API входа пользователя.

    При успешном входе возвращает access token,
    а refresh token кладёт в httpOnly cookie.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Выполняет вход пользователя.
        """

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = login_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            request=request,
        )

        response = Response(
            {
                "user": UserDetailSerializer(result["user"]).data,
                "access": result["access"],
            },
            status=status.HTTP_200_OK,
        )

        return set_refresh_token_cookie(
            response=response,
            refresh_token=result["refresh"],
        )


class RefreshTokenView(APIView):
    """
    API обновления access token.

    Refresh token читается из httpOnly cookie.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Возвращает новый access token.
        """

        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = refresh_access_token(request=request)

        response_serializer = AccessTokenSerializer(result)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    API выхода пользователя.

    Удаляет refresh cookie и, если возможно, заносит refresh token в blacklist.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Выполняет выход пользователя.
        """

        try:
            refresh_token = get_refresh_token_from_request(request)
            blacklist_refresh_token(refresh_token)
        except Exception:
            pass

        response = Response(status=status.HTTP_204_NO_CONTENT)

        return clear_refresh_token_cookie(response=response)


class VerifyEmailView(APIView):
    """
    API подтверждения email.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Подтверждает email по токену.
        """

        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = verify_email_token(
            token=serializer.validated_data["token"],
            request=request,
        )

        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_200_OK,
        )


class TeacherRegistrationView(APIView):
    """
    API регистрации преподавателя.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Регистрирует преподавателя через код приглашения.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Созданный пользователь.
        """

        serializer = TeacherRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = register_teacher(
            **serializer.validated_data,
            request=request,
        )

        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class LearnerRegistrationView(APIView):
    """
    API регистрации учащегося старше 14 лет.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Регистрирует учащегося.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Созданный пользователь.
        """

        serializer = LearnerRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = register_learner(
            **serializer.validated_data,
            request=request,
        )

        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class GuardianRegistrationView(APIView):
    """
    API регистрации родителя или законного представителя.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Регистрирует родителя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Созданный пользователь.
        """

        serializer = GuardianRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = register_guardian(
            **serializer.validated_data,
            request=request,
        )

        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class MinorLearnerRegistrationView(APIView):
    """
    API регистрации ребёнка младше 14 лет родителем.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Регистрирует ребёнка младше 14 лет.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Созданный пользователь ребёнка.
        """

        serializer = MinorLearnerRegistrationSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = register_minor_learner_by_guardian(
            guardian=request.user,
            **serializer.validated_data,
            request=request,
        )

        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class ForgotPasswordView(APIView):
    """
    API запроса восстановления пароля.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Отправляет письмо восстановления пароля, если email существует.
        """

        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_password_reset(
            email=serializer.validated_data["email"],
        )

        return Response(
            {
                "message": (
                    "Если аккаунт с таким email существует, мы отправили письмо "
                    "с инструкцией для восстановления доступа."
                )
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    """
    API установки нового пароля по токену восстановления.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Устанавливает новый пароль.
        """

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_password_by_token(
            token=serializer.validated_data["token"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {"message": "Пароль успешно обновлён. Теперь можно войти в аккаунт."},
            status=status.HTTP_200_OK,
        )
