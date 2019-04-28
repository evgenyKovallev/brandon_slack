from rest_framework import serializers
from core import models


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = ('email', 'unused', 'status')
