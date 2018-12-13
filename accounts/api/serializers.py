from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    EmailField,
    CharField,
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError
)

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email', required=True)
    email2 = EmailField(label='Confirm Email', required=True)
    password = CharField(style={'input_type': 'password'}, label='password', max_length=128, write_only=True,
                         required=True)
    password2 = CharField(style={'input_type': 'password'}, label='Confirm password', max_length=128, write_only=True,
                          required=True)

    class Meta:
        model = User
        fields = ['email', 'email2', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}, }

    def validate(self, attrs):
        email = attrs['email']
        user_qs = User.objects.filter(email=email)
        if user_qs:
            raise ValidationError('Email already used.')
        return attrs

    # def validate_email(self, value):
    #     data = self.get_initial()
    #     email2 = data.get('email2')
    #     email = value
    #     if email != email2:
    #         raise ValidationError("Emails do not match.")
    #     return value

    def validate_email2(self, value):
        data = self.get_initial()
        email = data.get('email')
        email2 = value
        if email != email2:
            raise ValidationError("Emails do not match.")
        return value

    # def validate_password(self, value):
    #     data = self.get_initial()
    #     password2 = data.get('password2')
    #     password = value
    #     if password != password2:
    #         raise ValidationError("Passwords do not match.")
    #     return value

    def validate_password2(self, value):
        data = self.get_initial()
        password = data.get('password')
        password2 = value
        if password != password2:
            raise ValidationError("Passwords do not match.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(email=email)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label='Email', required=True)
    password = CharField(style={'input_type': 'password'}, label='password', write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}, }

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        user = User.objects.filter(email=email)

        if user.exists() and user.count() == 1:
                user = user.first()
        else:
            raise ValidationError("Invalid email")

        if user:
            if not user.check_password(password):
                raise ValidationError('Invalid email or password.')

        attrs['token'] = 'TOKEN STRING  '

        return attrs


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
        ]
