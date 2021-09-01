from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from users.models import CustomUser as User
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.filters import BaseFilterBackend
import coreapi
from drf_yasg import openapi




class PropsalViewTwo(APIView):
    def get(self, request,pk):
        Proposals_type=models.Services.objects.filter(vendor_id=pk).values_list("service_image")
        return Response(Proposals_type)



class PropsalView(APIView):
    def get(self, request):
        get_data=request.query_params
        search_text = get_data.get("filter")
        if search_text:
            Proposals_type=models.Proposals.objects.filter(Proposals_type=search_text)
            count=Proposals_type.count()
            serializer = serializers.ProposalUserSerializer(Proposals_type, many=True)
            return Response( {
                    "proposals":search_text,
                    "count":count,
                    "result":serializer.data})
         
        else:
            search_text = get_data.get("user_id")
            Proposals=models.Proposals.objects.filter(user_id=search_text)
            order=models.Order.objects.filter(user_id=search_text)
            services=models.Vendors.objects.filter(user_id=search_text)
            serializer1 = serializers.ProposalUserSerializer(Proposals, many=True)
            serializer2 = serializers.OrderUserSerializer(order, many=True)
            #serializer3 = serializers.VendorListSerializer(services, many=True)
            response=serializer1.data+serializer2.data
            return Response(response)
               

class VendorReviewView(APIView):
    def get(self, request):
        get_data=request.query_params
        ID = get_data.get("vendor_id")
        objects = models.VendorsReview.objects.filter(vendor_id=ID)
        serializer = serializers.VendorsReviewserializer(objects, many=True)
        return Response({
                         "Vandor_id":ID,
                         "reviews":serializer.data})
    
class ServiceListView(APIView):
    def get(self, request):
        objects = models.Services.objects.all()
        serializer = serializers.ServiceSerializer(objects, many=True)
        return Response(serializer.data)
    

    
class VendorServiceView(APIView):
    def get(self, request):
        get_data=request.query_params
        ID = get_data.get("vendor_id")
        objects = models.Services.objects.filter(vendor_id=ID)
        serializer = serializers.ServiceSerializer(objects, many=True)
        return Response({
            "vendor_id":ID,
            "Services":serializer.data}
                        
        )



class VendorListView(APIView):
    def get(self, request):
        objects = models.Vendors.objects.all()
        serializer = serializers.VendorListSerializer(objects, many=True)
        return Response(serializer.data)




class EventsTypeView(APIView):
    def get(self, request):
        objects = models.Events.objects.all()
        serializer = serializers.EventsSerializer(objects, many=True)
        return Response(serializer.data)



# Create your views here.
class RoomView(APIView):
    def get(self,request):
        text=request.GET.get("filter")
        room=models.Room.objects.filter(room_type=text)
        count=room.count()
        Serializers=serializers.RoomSerializer(room,many=True)
        return Response({"Room_Type":text,
                            "count":count,
                            "result":Serializers.data}
            )
        
    
    def get_serializer(self):
        return serializers.RoomPostSerializer()
    
    def post(self,request):
        Serializers=serializers.RoomPostSerializer(data=request.data)
        if Serializers.is_valid():
            Serializers.save()
            return Response(Serializers.data)
        else:
            return Response(Serializers.errors,status=status.HTTP_400_BAD_REQUEST)
