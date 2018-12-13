from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    CharField,
)

from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentSerializer
from posts.models import Post
from comments.models import Comment

post_detail_url = HyperlinkedIdentityField(
    view_name='posts-api:post-detail',
    lookup_field='slug',
)
post_edit_url = HyperlinkedIdentityField(
    view_name='posts-api:post-update',
    lookup_field='slug',
)


class PostSerializer(ModelSerializer):
    # slug = serializers.CharField(label='slug', required=False)
    content = CharField(label='content', required=False)
    url = post_detail_url

    class Meta:
        model = Post
        # fields = ['title', 'slug', 'content']
        fields = ['id', 'slug', 'url', 'title', 'content',]
        # fields = ['title', 'content']


class PostDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    content = CharField(label='content', required=False)
    url = post_detail_url
    edit_url = post_edit_url
    image = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['url', 'user', 'title', 'content', 'edit_url', 'image', 'comments']

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None

        return image

    def get_comments(self, obj):
        # content_type = obj.get_content_type
        # object_id = obj.object_id
        querysets = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(querysets, many=True).data
        return comments
