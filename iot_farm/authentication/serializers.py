from users.serializers import UserGenericSerializer
from users.models import User


class ProfileSerializer(UserGenericSerializer):

    class Meta(UserGenericSerializer.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'mobile',
                  'address', 'avatar', 'date_joined', 'last_login', )
        read_only_fields = ('username', 'email', 'date_joined', 'last_login', )
