from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.responses import ApiResponse

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)


@extend_schema(
    tags=["Authentication"],
    summary="Register User",
    description="Create a new user account.",
    request=RegisterSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiResponse(
            description="Validation Error"
        ),
    },
)
class RegisterView(APIView):

    serializer_class = RegisterSerializer

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return ApiResponse.success(
            data=serializer.data,
            message="User registered successfully.",
            status_code=status.HTTP_201_CREATED,
        )


@extend_schema(
    tags=["Authentication"],
    summary="Login",
    description="Authenticate user and return JWT tokens.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Login successful"
        ),
        400: OpenApiResponse(
            description="Invalid credentials"
        ),
    },
)
class LoginView(APIView):

    serializer_class = LoginSerializer

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return ApiResponse.success(
            data=serializer.validated_data,
            message="Login successful.",
        )


@extend_schema(
    tags=["Authentication"],
    summary="My Profile",
    description="Return authenticated user's profile.",
    responses={
        200: UserSerializer,
    },
)
class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer

    def get(self, request):

        serializer = UserSerializer(
            request.user
        )

        return ApiResponse.success(
            data=serializer.data,
            message="Profile fetched successfully.",
        )