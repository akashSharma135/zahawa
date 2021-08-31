from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import models

# Create your views here.
class RoomView(APIView):
    def get(self,request):
        text=request.GET.get("filter")
        room=models.Room.objects.filter(room_type=text)
        count=room.count()
        if room:
            Serializers=serializers.RoomSerializer(room,many=True)
            return Response({"Room_Type":text,
                            "count":count,
                            "result":Serializers.data}
            )
        return Response("NOT_FOUND" , status=status.HTTP_404_NOT_FOUND)
    
    def get_serializer(self):
        return serializers.RoomPostSerializer()
    
    def post(self,request):
        Serializers=serializers.RoomPostSerializer(data=request.data)
        if Serializers.is_valid():
            Serializers.save()
            return Response(Serializers.data)
        else:
            return Response(Serializers.errors,status=status.HTTP_400_BAD_REQUEST)
