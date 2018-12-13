from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


from comments.models import Comment
User = get_user_model()


def file_upload_location(instance, filename):
    post_model = instance.__class__
    new_id = post_model.objects.order_by("id").last().id + 1
    return "{}/{}".format(new_id, filename)


class Post(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=file_upload_location, null=True, blank=True,)
    content = models.TextField()
    publish = models.DateField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:post-detail", kwargs={'slug': self.slug})

    def get_api_url(self):
        return reverse("posts-api:post-detail",  kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    @property
    def comments(self):
        qs = Comment.objects.filter_by_instance(self)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "{}-{}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Post)
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
