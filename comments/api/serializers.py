from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    CharField,
)

from accounts.api.serializers import UserDetailSerializer

from comments.models import Comment
User = get_user_model()


def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = ['id', 'content']

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            self.user = user
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() and model_qs.count() != 1:
                raise ValidationError("Invalid Content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() and obj_qs.count() != 1:
                raise ValidationError('Slug invalid or not found')
            return data

        def create(self, validated_data):
            content = validated_data.get('content')
            if self.user:
                main_user = self.user
            else:
                main_user = user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type,
                slug,
                content,
                main_user,
                parent_obj=parent_obj
            )
            return comment

    return CommentCreateSerializer


class CommentSerializer(ModelSerializer):
    replies = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content_type', 'object_id', 'parent', 'content', 'replies']

    def get_replies(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='comments-api:thread')
    replies = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['url', 'id', 'content', 'replies']

    def get_replies(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'timestamp']


class CommentDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    replies = SerializerMethodField()
    content_object_url = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            # 'content_type',
            # 'object_id',
            'content',
            'timestamp',
            'replies',
            'content_object_url'
        ]
        read_only_fields = [
            # 'content_type',
            # 'object_id',
            'replies'
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None
