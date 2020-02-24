from rest_framework import parsers, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.utils import aware_utcnow
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User
from .serializers import ProfileSerializer


# Create your views here.
class LogoutView(CreateAPIView, JWTAuthentication):
    """
    Logout of system.
    """
    queryset = OutstandingToken.objects.all()
    serializer_class = TokenRefreshSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
        except TokenError as err:
            return Response(data={'detail': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            serializer = self.get_serializer_class()(data=request.data)
            if serializer.is_valid() is False:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        login_user = self.authenticate(request)[0]
        self.get_queryset().filter(expires_at__lte=aware_utcnow(), user=login_user).delete()

        return Response(status=status.HTTP_200_OK)


class ProfileView(RetrieveUpdateAPIView, JWTAuthentication):
    """
    User get and update Profile by himself or herself.
    """
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, ]
    parser_classes = [parsers.MultiPartParser, ]

    def retrieve(self, request, *args, **kwargs):
        login_user = self.authenticate(request)[0]
        serializer = self.get_serializer(login_user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        login_user = self.authenticate(request)[0]
        serializer = self.get_serializer(login_user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(login_user, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            login_user._prefetched_objects_cache = {}

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
