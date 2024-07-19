from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True) 
    interests = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_suspended = models.BooleanField(default=False)
    likes_count = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    premium_ends = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return str(self.user)
    
    @property
    def name(self):
        if self.displayname:
            return self.displayname
        return self.user.username 
    
    @property
    def is_subscribed(self):
        if self.is_premium:
            return True
        return False
    @property
    def is_verified(self):
        if self.is_verified:
            return True
        return False
    
    @property
    def likes(self):
        return self.likes_count
    
    @property
    def is_suspended(self):
        if self.is_suspended:
            return True
        return False
    

    @property
    def mobile(self):
        if self.phone:
            return self.phone
        return None
    
    @property
    def avatar(self):
        if self.image:
            return self.image.url
        return static("images/avatar.svg")
