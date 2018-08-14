from __future__ import unicode_literals
from datetime import datetime
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Basemodel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.date_modified = datetime.now()
        super(Basemodel, self).save(*args, **kwargs)

    class Meta:
        abstract = True      # abstact class

class Userprofile(Basemodel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    extra = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    uuid = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance)