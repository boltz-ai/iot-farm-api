from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.permissions import IsSuperUserPermission
from . import settings as user_settings
from .models import User
from .serializers import UserGenericSerializer, UserChangePasswordSerializer, UserCreateSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    User APIs, handled by `superuser` role.
    This viewset automatically provides `list`, `create`, `retrieve`, `update`, `destroy` and `change_password` actions.
    """
    queryset = User.objects.exclude(is_superuser=True).order_by('username')
    serializer_class = UserGenericSerializer
    permission_classes = [IsAuthenticated & IsSuperUserPermission]
    search_fields = ['username', 'email', ]
    filter_fields = ('is_active', )

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'change_password':
            return UserChangePasswordSerializer
        return UserGenericSerializer

    @action(methods=['post'], detail=True, url_path='change-password', url_name='change_password',
            permission_classes=[IsSuperUserPermission])
    def change_password(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        instance.set_password(serializer.validated_data['password'])
        instance.save()
        return Response(
            {
                'detail': 'The user password changed successfully'
            },
            status=status.HTTP_200_OK
        )
