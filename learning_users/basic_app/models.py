from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # additional classes
    portfolio_site = models.URLField(blank=True) # blank=True makes it optional
    # upload_to points to your media folder
        # so profile_pics needs to be a subdirectory beneath our media folder.
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True) 

    def __str__(self):
        return self.user.username # username is a default attribute of the User built-in class.
