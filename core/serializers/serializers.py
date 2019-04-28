from rest_framework import serializers
from .. import models


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = ('email', 'unused', 'status')
