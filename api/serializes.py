from rest_framework import fields, serializers
from rest_framework.reverse import reverse
from .models import *

class UserSubcriberNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubcriberNews
        fields = ('name','email')