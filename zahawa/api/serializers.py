from rest_framework import serializers

from api import  models

class RoomSerializer(serializers.ModelSerializer):
    count=serializers.SerializerMethodField()
    class Meta:
        model = models.Room
        fields =['room','count',]
    def get_count(self,obj):
        count=models.Room.objects.filter(room_type=obj.room_type).count()
        return count
    
    
class RoomPOSTSerializer(serializers.ModelSerializer):
     class Meta:
        model = models.Room
        fields =['room','room_type','subscribers',]
