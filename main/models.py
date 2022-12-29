from django.db import models
from django.contrib.auth.models import User, Group
import uuid
# Create your models here.

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logos', null=True, blank=True)
    def __str__(self):
        return self.name

class Representative(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " - " + self.organization.name + " - " + self.designation

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    img_file = models.ImageField(upload_to='certificates', null=True, blank=True)
    generation_time = models.DateTimeField(auto_now_add=True)
    is_revoked = models.BooleanField(default=False)
    revokation_reason = models.CharField(max_length=100, null=True, blank=True)
    revokation_time = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.name