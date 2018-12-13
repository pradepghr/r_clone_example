from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, blank=True)
    karma = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile/profile_images', max_length=254, blank=True)
    country = models.CharField(max_length=30, blank=True)
    created_on = models.DateField(null=True, editable=False)
    updated_on = models.DateField(null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()
        return super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    profile = Profile.objects.get(user=instance)
    profile.save()
