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
from django.shortcuts import render, get_object_or_404



class SearchFilterOrder(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="Keyword", location="query", required=False, type="string"
            )
        ]
class SearchFilterOrderView(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="user_id", location="query", required=False, type="id"
            )
        ]


class SearchFilterVendor(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="vendor_id", location="query", required=False, type="id"
            )
        ]
class SearchFilterloyalty(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="room ", location="query", required=False, type="id"
            ),
               coreapi.Field(
                name="room_type ", location="query", required=False, type="id"
            )
        

        ]
class SearchFilterApiSearch(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="name ", location="query", required=False, type="id"
            ),
               coreapi.Field(
                name="description ", location="query", required=False, type="id"
            ),
               coreapi.Field(
                name="service_name ", location="query", required=False, type="id"
            )
        

        ]





class TeamView(APIView):
    def get(self, request,pk):
        objects= models.Team.objects.filter(pk=pk)
        serializer= serializers.TeamListSerializer(objects,many=True)
        return Response(serializer.data)
    
    
    def get_serializer(self):
        properties = {
            "thumb": openapi.Schema(
                type=openapi.TYPE_STRING, description="Image"
            ),
            "name": openapi.Schema(
                type=openapi.TYPE_STRING, description="string"
            )
        }
        return_openapi_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT, properties=properties
        )
        return return_openapi_schema
    def patch(self, request,pk):
        objects = get_object_or_404(
            models.Team.objects.filter(pk=pk))
        serializer = serializers.TeamListSerializer(
            objects, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class UserCartView(APIView):
    def get_serializer(self):
        return serializers.UserCartSerializer()
    def post(self, request):
        serializer= serializers.UserCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class OrderCartView(APIView):
    def get_serializer(self):
        return serializers.OrderCartSerializer()
    def post(self, request):
        serializer= serializers.OrderCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        



class OrderSearchViewFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="keyword",
                location="query",
                required=False,
                type="string",
                description="send search keyword",
            )
        ]


#search order by keyword
class OrderSearchView(APIView):
    filter_backends = (OrderSearchViewFilterBackend,)
    def get(self, request):
        keyword=request.GET.get("keyword")
        if keyword=="Active":
            objects=models.Order.objects.filter(order_Type__contains=keyword)
            serializer =serializers.OrderSerializer(objects,many=True)
            return Response({"Keyword":keyword,
                            "count":objects.count(),
                            "result":serializer.data})
        if keyword=="Completed":
            objects=models.Order.objects.filter(order_Type__contains=Completed)
            serializer =serializers.OrderSerializer(objects,many=True)
            return Response({"Keyword":keyword,
                            "count":objects.count(),
                            "result":serializer.data})

        else:
            objects=models.Order.objects.filter(Q(order_Type="Active")|Q(order_Type="Completed"))
            serializer =serializers.OrderSerializer(objects,many=True)
            return Response(serializer.data)
            
#all orders detail view
class OrderDetailsView(APIView):
    def get(self, request):
        objects = models.Order.objects.all()
        # objects = models.Order.objects.filter(user=request.user)
        serializer= serializers.OrderSerializer(objects,many=True)
        return Response(serializer.data)

#order by user id view
class UserOrderDView(APIView):
    filter_backends = (SearchFilterOrderView,)
    def get(self, request):
        ID=request.GET.get("user_id")
        objects = models.Order.objects.filter(user=ID)
        # objects = models.Order.objects.filter(user=request.user)
        serializer= serializers.OrderSerializer(objects,many=True)
        return Response(serializer.data)

    def get_serializer(self):
        return serializers.postOrderSerializer()

    def post(self, request):
        serializer= serializers.postOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        

class VendorTypeView(APIView):
    def get(self, request):
        objects = models.Vendors.objects.all()  
        serializer= serializers.VendorsTypeSerializers(objects,many=True)
        return Response({
            "result":serializer.data
            })
    
#view for list all Categories 
class CategoriesView(APIView):
    def get(self, request):
        objects = models.Categories.objects.all()  
        serializer= serializers.CategoriesSerializers(objects,many=True)
        return Response({
            "Categories":serializer.data
            })
    
class CategoriesDetailsView(APIView):
    def get(self, request,pk):
        objects = models.Vendors.objects.filter(categories=pk)
        serializer= serializers.DetailsSerializers(objects,many=True)
        return Response({"Categorie_id":pk,
                         "result":serializer.data})
        
    

class loyaltySearchViewFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="room",
                location="query",
                required=False,
                type="string",
                description="send search keyword",
            ),
            coreapi.Field(
                name="room_type",
                location="query",
                required=False,
                type="string",
                description="send description keyword",
            )
        ]


#view for loyaltySearch by keywords and count
class loyaltySearchView(APIView):
    filter_backends = (loyaltySearchViewFilterBackend,)
    def get(self, request):
        room=request.GET.get("room")
        room_type=request.GET.get("room_type")
        if room: 
            objects=models.Room.objects.filter(room__contains=room)
            Count=objects.count()
            Serializers=serializers.RoomSerializer(objects,many=True)
            return Response({
                "keyword":room,
                "cont":Count,
                "result":Serializers.data})    
        if room_type:
            objects=models.Room.objects.filter(room_type__contains=room_type)
            Count=objects.count()
            Serializers=serializers.RoomSerializer(objects,many=True)
            return Response({
                    "keyword":room_type,
                    "cont":Count,
                    "result":Serializers.data}) 


class ApiSearchViewFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="name",
                location="query",
                required=False,
                type="string",
                description="send search keyword",
            ),
            coreapi.Field(
                name="description",
                location="query",
                required=False,
                type="string",
                description="send description keyword",
            )
        ]


class ApiSearchView(APIView):
    filter_backends = (ApiSearchViewFilterBackend,)
    def get(self, request):
        name=request.GET.get("name")
        description=request.GET.get("description")
        if name: 
            objects=models.Vendors.objects.filter(name__contains=name)
            Count=objects.count()
            Serializers=serializers.VendorsSerializers(objects,many=True)
            return Response({
                "keyword":name,
                "cont":Count,
                "result":Serializers.data})    
        if description:
            objects=models.Vendors.objects.filter(description__contains=description)
            Count=objects.count()
            Serializers=serializers.VendorsSerializers(objects,many=True)
            return Response({
                    "keyword":description,
                    "cont":Count,
                    "result":Serializers.data})   
            
        service_name=request.GET.get("service_name")
        if service_name:
            objects=models.Services.objects.filter(service_name__contains=service_name) 
            Serializers=serializers.ServicesSerializers(objects,many=True)
            return Response({
                        "keyword":service_name,
                        "cont":Count,
                        "result":Serializers.data})  
        


class PropsalViewFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="filter",
                location="query",
                required=False,
                type="string",
                description="send search keyword",
            ),
            coreapi.Field(
                name="user_id",
                location="query",
                required=False,
                type="string",
                description="send search keyword",
            )
        ]


class PropsalView(APIView):
    filter_backends = (PropsalViewFilterBackend,)
    def get(self, request):
        get_data=request.query_params
        search_text = get_data.get("keyword")
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
            response=serializer1.data+serializer2.data
            return Response(response)

    def get_serializer(self):
        return serializers.ProposalUserSerializer()

    def post(self,request):
        Serializers =serializers.ProposalUserSerializer(data=request.data)
        if Serializers.is_valid():
            Serializers.save()
            return Response(Serializers.data)
        return Response(Serializers.errors)


class VendorReviewFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="vendor_id",
                location="query",
                required=False,
                type="string",
                description="send search keyword",
            )
        ]


class VendorReviewView(APIView):
    filter_backends = (SearchFilterVendor,)
    def get(self, request):
        filter_backends = (VendorReviewFilterBackend,)
        get_data=request.query_params
        ID = get_data.get("vendor_id")
        if ID:
            objects = models.VendorsReview.objects.filter(vendor_id=ID)
            serializer = serializers.VendorsReviewserializer(objects, many=True)
            return Response({
                            "Vandor_id":ID,
                            "reviews":serializer.data})
        else:
            objects = models.VendorsReview.objects.all()
            serializer = serializers.VendorsReviewserializer(objects, many=True)
            return Response({"reviews":serializer.data})
            
class ServiceListView(APIView):
    def get(self, request):
        objects = models.Services.objects.all()
        serializer = serializers.ServiceSerializer(objects, many=True)
        return Response(serializer.data)
    

    
#----------Have to fix-----------------   
#-----------vendor_id-----------#
        #----------------#

# class VendorServiceView(APIView):
#     def get(self, request):
#         get_data=request.query_params
#         ID = get_data.get("vendor_id")
#         objects = models.Services.objects.filter(vendor_id=ID)
#         serializer = serializers.ServiceSerializer(objects, many=True)
#         return Response({
#             "vendor_id":ID,
#             "Services":serializer.data}
                        
#         )



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


class RoomFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="filter",
                location="query",
                required=True,
                type="string",
                description="send search keyword",
            )
        ]


# Create your views here.
class RoomView(APIView):
    filter_backends = (RoomFilterBackend,)
    def get(self,request):
        text=request.GET.get("keyword")
        room=models.Room.objects.filter(room_type=text)
        count=room.count()
        Serializers=serializers.RoomSerializer(room,many=True)
        return Response({"room_type":text,
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
