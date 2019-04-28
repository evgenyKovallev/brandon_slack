from django.db import models


class Email(models.Model):
    email = models.CharField(max_length=255, unique=True)
    unused = models.BooleanField(default=True)
    status = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True)
