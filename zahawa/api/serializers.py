from rest_framework import serializers

from api import  models

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields =['id','room',]
   
class RoomPostSerializer(serializers.ModelSerializer):
     class Meta:
        model = models.Room
        fields =['room','room_type','subscribers',]
