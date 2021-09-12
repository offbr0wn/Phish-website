from django.db import models
from django.contrib.auth.models import User

from PIL import Image


# Main model for users account restricts certain user attributes to a max number of characters
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # username = models.CharField(max_length=40, null=True)
    email = models.EmailField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


class Tag(models.Model):
    username = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user.username

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
