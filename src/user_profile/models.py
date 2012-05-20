from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    share_predictions = models.PositiveSmallIntegerField(default=0)
    class Meta:
        db_table = u"users"
        
# Automatically create a UserProfile object whenever a User object is created.. 
from django.db.models.signals import post_save
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)