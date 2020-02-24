from rest_framework import serializers

from . import models, settings as user_settings


# Serializer for set password
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.RegexField(
        regex=user_settings.PASSWORD_REGEX_4, min_length=8, max_length=128, allow_blank=False, allow_null=False, )

    class Meta:
        fields = ('password', )
        extra_kwargs = {'password': {'write_only': True}}


class UserGenericSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'mobile', 'address', 'avatar',
            'created_at', 'date_joined', 'last_login', 'is_active', 'updated_at', 'deleted_at',
        )
        read_only_fields = ('id', 'username', 'email', 'avatar', 'created_at', 'date_joined',
                            'last_login', 'updated_at', 'deleted_at', )


class UserCreateSerializer(UserGenericSerializer, UserChangePasswordSerializer):

    class Meta(UserChangePasswordSerializer.Meta):
        model = models.User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'mobile', 'address', )
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
