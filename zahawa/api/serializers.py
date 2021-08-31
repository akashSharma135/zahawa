from rest_framework import serializers
from . import models


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Events
        fields = "__all__"



class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields =['id','room',]
   
class RoomPostSerializer(serializers.ModelSerializer):
     class Meta:
        model = models.Room
        fields =['room','room_type','subscribers',]
