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
        obj=models.Room.objects.filter(room_type=text)
        if obj:
            Serializers=serializers.RoomSerializer(obj,many=True)
            return Response(Serializers.data[0])
        return Response("NO_CONTENT" , status=status.HTTP_204_NO_CONTENT)
    
    def get_serializer(self):
        return serializers.RoomPOSTSerializer()
    
    def post(self,request):
        Serializers=serializers.RoomPOSTSerializer(data=request.data)
        if Serializers.is_valid():
            Serializers.save()
            return Response(Serializers.data)
        else:
            return Response(Serializers.errors,status=status.HTTP_204_NO_CONTENT)
