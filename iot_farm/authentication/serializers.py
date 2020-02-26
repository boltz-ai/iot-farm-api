from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.serializers import UserGenericSerializer
from users.models import User


class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        self.user.last_login = timezone.now()
        self.user.save()

        return data


class ProfileSerializer(UserGenericSerializer):

    class Meta(UserGenericSerializer.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'mobile',
                  'address', 'avatar', 'date_joined', 'last_login', )
        read_only_fields = ('username', 'email', 'date_joined', 'last_login', )
