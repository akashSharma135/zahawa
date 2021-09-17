from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
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
                name="keyword", location="query", required=False, type="string"
            )
        ]
class SearchFilterOrderView(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="user_id", location="query", required=False, type="id"
            )
        ]


# class SearchFilterVendor(BaseFilterBackend):
#     def get_schema_fields(self, view):
#         return [
#             coreapi.Field(
#                 name="vendor_id", location="query", required=False, type="id"
#             )
#         ]
class SearchFilterloyalty(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="room", location="query", required=False, type="id"
            ),
               coreapi.Field(
                name="room_type", location="query", required=False, type="id"
            )


        ]
class SearchFilterApiSearch(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="name", location="query", required=False, type="id"
            ),
               coreapi.Field(
                name="description", location="query", required=False, type="id"
            ),
               coreapi.Field(
                name="service_name", location="query", required=False, type="id"
            )
        

        ]

class SearchProposalBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="Proposals_type", location="query", required=False, type="string"
            ),
            coreapi.Field(
                name="user_id", location="query", required=False, type="id"
            )
        ]
        

class ServicePackageFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="vendor_id", location="query", required=False, type="id"
            ),
            coreapi.Field(
                name="service_id", location="query", required=False, type="id"
            )
        ]

class ServicePackageView(APIView):
    filter_backends = (ServicePackageFilterBackend,)
    def get(self, request,):
        vendor_id=request.GET.get("vendor_id")
        service_id=request.GET.get("service_id")
        objects=models.Services.objects.filter(pk=service_id,vendors=vendor_id)
        serializer= serializers.ServicePackageSerializer(objects,many=True)
        return Response(serializer.data)

class Order(APIView):
    def get(self, request,pk):
        ID=request.GET.get("user_id")
        objects=models.Order.objects.filter(user=ID)
        serializer= serializers.OrderListserializer(objects,many=True)
        return Response(serializer.data)

class TeamView(APIView):
    def get(self, request,pk):
        objects= models.Team.objects.filter(pk=pk)
        serializer= serializers.TeamListSerializer(objects,many=True)
        return Response(serializer.data)
    
    
    # def get_serializer(self):
    #     properties = {
    #         "thumb": openapi.Schema(
    #             type=openapi.TYPE_STRING, description="Image"
    #         ),
    #         "name": openapi.Schema(
    #             type=openapi.TYPE_STRING, description="string"
    #         )
    #     }
    #     return_openapi_schema = openapi.Schema(
    #         type=openapi.TYPE_OBJECT, properties=properties
    #     )
    #     return return_openapi_schema
    def patch(self, request,pk):
        objects = get_object_or_404(
            models.Team.objects.filter(pk=pk))
        serializer = serializers.TeamListSerializer(
            objects, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response({"Team Updated":serializer.data})


class UserCartView(APIView):
    def get_serializer(self):
        return serializers.UserCartSerializer()
    def post(self, request):
        serializer= serializers.UserCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class MycartOrderFilter(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="cart_id", location="query", required=False, type="id"
            )
        ]

class MyCartView(APIView):
    def get(self, request):
        objects=models.CartItem.objects.filter(cart__user=request.user)
        serializer= serializers.MyCartSerializer(objects,many=True)
        return Response(serializer.data)
    
    def get_serializer(self):
        return serializers.MyCartPostSerializer()
    
    def post(self,request):
        serializer=serializers.MyCartPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "New event cart created",
                            "Result":serializer.data})
        else:
            return Response(serializer.errors)
            
    def delete(self,request,pk):
        ID=request.GET.get("cart_id")
        objects=models.CartItem.objects.filter(pk=pk).delete()
        return Response("NO_CONTENT",status=status.HTTP_204_NO_CONTENT)



#search order by keyword
class OrderSearchView(APIView):
    filter_backends = (SearchFilterOrder,)
    def get(self, request):
        filters=request.GET.get("filter")
        keyword=request.GET.get("keyword")
        serializer=[]; 
        Count=0
        if filters or keyword:
            objects1=models.Order.objects.filter(delivery_address__contains=keyword,order_status=filters)
            Count =objects1.count()
            serializer=serializers.RoomSerializer(objects1,many=True).data
        return Response({
                "keyword":keyword,
                "filter":filters,
                "cont":Count,
                "result":serializer})    
        

#all orders detail view
# class OrderDetailsView(APIView):
#     def get(self, request):
#         objects = models.Order.objects.all()
#         # objects = models.Order.objects.filter(user=request.user)
#         serializer= serializers.OrderSerializer(objects,many=True)
#         return Response(serializer.data)

#order by user id view
class UserOrderView(APIView):
    filter_backends = (SearchFilterOrderView,)
    permission_classes = [IsAuthenticated]
    def get(self, request):
        ID=request.GET.get("user_id")
        if ID:
            objects = models.Order.objects.filter(user=ID)
            serializer= serializers.OrderSerializer(objects,many=True)
            return Response(serializer.data)
        else:
            objects = models.Order.objects.filter(user=request.user)
            serializer= serializers.OrderSerializer(objects,many=True)
            return Response(serializer.data)
            
            
    # def get_serializer(self):
    #     return serializers.postOrderSerializer()

    # def post(self, request):
    #     serializer= serializers.postOrderSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors)
        

class VendorTypeView(APIView):
    def get(self, request):
        objects = models.Vendors.objects.all()  
        serializer= serializers.VendorsTypeSerializers(objects,many=True)
        return Response({
            "result":serializer.data
            })
    
# favourite vendors
class FavouriteVendorView(APIView):
    def get(self, request):
        objects = models.Vendors.objects.filter(user_id=request.user.id, is_favourite=True)
        serializer = serializers.VendorsSerializers(objects, many=True)
        return Response(serializer.data)

# Favourite products
class FavouriteProductView(APIView):
    def get(self, request):
        objects = models.Product.objects.filter(user_id=request.user.id).filter(is_favourite=True)
        serializer = serializers.ProductSerializer(objects, many=True)
        return Response(serializer.data)

# Favourite services
class FavouriteServiceView(APIView):
    def get(self, request):
        objects = models.Services.objects.filter(user_id=request.user.id).filter(is_favourite=True)
        serializer = serializers.ServiceSerializer(objects, many=True)
        return Response(serializer.data)

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
        Serializer=[]; 
        Count1=0
        Count2=0
        if room: 
            objects=models.Room.objects.filter(room__contains=room)
            Count1=objects.count()
            Serializers1=serializers.RoomSerializer(objects,many=True).data
            Serializer=Serializer+Serializers1
     
        if room_type:
            objects=models.Room.objects.filter(room_type__contains=room_type)
            Count2=objects.count()
            Serializers2=serializers.RoomSerializer(objects,many=True).data
            Serializer=Serializer+Serializers2
        return Response({
                "keyword1":room_type,
                "cont1":Count1,
                "keyword2":room,
                "cont2":Count2,
                "result":Serializer
                }) 


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
        name_search=request.GET.get("name")
        description=request.GET.get("description")
        service_name=request.GET.get("service_name")
        product_name=request.GET.get("product")
        count1=0
        count2=0
        count3=0
        count4=0
        Services=[]; 
        Vendors=[]; 
        Product=[]; 
        if name_search: 
            objects=models.Vendors.objects.filter(name__contains=name_search)
            count1=objects.count()
            Serializers1=serializers.VendorsSerializers(objects,many=True).data
            Vendors=Vendors+Serializers1
          
        if description:
            objects=models.Vendors.objects.filter(description__contains=description)
            count2=objects.count()
            Serializers2=serializers.VendorsSerializers(objects,many=True).data
            Vendors=Vendors+Serializers2
            
        if service_name:
            objects=models.Services.objects.filter(service_name__contains=service_name) 
            count3=objects.count()
            Serializers3=serializers.ServicesSerializers(objects,many=True).data
            Services=Services+Serializers3
        if product_name:
            objects=models.Product.objects.filter(product_name__contains=product_name) 
            count4=objects.count()
            Serializers4=serializers.ProductSerializer(objects,many=True).data
            Product=Product+Serializers4
        return Response({
	            "vendors": {"keyword1":name_search , "count1":count1 ,"keyword2":description , "count2":count2 ,"result": [Vendors]},
	            "services": {"keyword": service_name, "count": count3, "result": [Services]},
                "products": {"keyword": product_name, "count":count4, "result": [Product]},
                        })
        
   

class PropsalViewFilterBackend(BaseFilterBackend):
    filter_backends = (SearchProposalBackend,)
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="keyword",
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
        count=0
        serializer=[]; 
        if search_text:
            Proposals_type=models.Proposals.objects.filter(Proposals_type=search_text)
            count=Proposals_type.count()
            serializer1 = serializers.ProposalUserSerializer(Proposals_type, many=True).data
            serializer=serializer+serializer1
        return Response( {
            "proposals":search_text,
            "count":count,
            "result":serializer})
        
class PropsalUserView(APIView):
    def get(self, request,pk):
        Proposals=models.Proposals.objects.filter(user_id=pk)
        Events=models.Events.objects.filter(Packages__vendors__user_id=pk)
        services=models.Vendors.objects.filter(user_id=pk)
        serializer1 = serializers.ProposalUserSerializer(Proposals, many=True)
        serializer2 = serializers.EventsUserSerializer(Events, many=True)
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


# class VendorReviewFilterBackend(BaseFilterBackend):
#     def get_schema_fields(self, view):
#         return [
#             coreapi.Field(
#                 name="vendor_id",
#                 location="query",
#                 required=False,
#                 type="string",
#                 description="send search keyword",
#             )
#         ]


class VendorReviewView(APIView):
    def get(self, request,pk):
        objects = models.VendorsReview.objects.filter(vendor_id=pk)
        serializer = serializers.VendorsReviewserializer(objects, many=True)
        return Response({"reviews":serializer.data})
            
class ServiceListView(APIView):
    def get(self, request):
        objects = models.Services.objects.all()
        serializer = serializers.ServiceSerializer(objects, many=True)
        return Response(serializer.data)
    

    
class VendorServiceView(APIView):
    def get(self, request,pk):
        objects = models.Services.objects.filter(vendors_id=pk)
        serializer = serializers.ServiceSerializer(objects, many=True)
        return Response({
            "vendor_id":pk,
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
