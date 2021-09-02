from rest_framework import serializers
from . import models
from django.db.models import Avg
from rest_framework.response import Response




class Vendors(serializers.ModelSerializer):
    class Meta:
        model = models.Vendors
        fields = "__all__"

class Services(serializers.ModelSerializer):
    class Meta:
        model = models.Services
        fields = "__all__"

class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['event_title','event_type','event_date','event_time','event_location','total_amount']
class ProposalUserSerializer(serializers.ModelSerializer):
    service_name= serializers.SerializerMethodField()
    class Meta:
        model = models.Proposals
        fields = ['user','Proposals_type','Proposals_status','title','created','service_name',]
    def get_service_name(self,obj):
        service_name = models.Services.objects.filter().values_list("service_name",flat=True)
        return service_name


        
class VendorsReviewserializer(serializers.ModelSerializer):
    user_image= serializers.SerializerMethodField()
    class Meta:
        model = models.VendorsReview
        fields = ['user','user_image','rating','description']
        
    def get_user_image(self, obj):
        image = models.CustomUser.objects.filter(profile_picture=obj.user.id)
        return image

class ServiceSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    class Meta:
        model = models.Services
        fields = ['service_image','rating','service_name','service_minAmount','service_maxAmount']
    def get_rating(self, obj):
        rating = models.VendorsReview.objects.filter(vendor=obj.id).aggregate(
            Avg("rating")
        )
        return str(rating["rating__avg"])

class VendorListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    priject_images=serializers.SerializerMethodField()
    user_image=serializers.SerializerMethodField()
    class Meta:
        model = models.Vendors
        fields = "__all__"
    def get_avg_rating(self, obj):
        avg_rating = models.VendorsReview.objects.filter(vendor=obj.id).aggregate(
            Avg("rating")
        )
        return str(avg_rating["rating__avg"])
    
    def get_rating(self, obj):
        rating = models.VendorsReview.objects.values_list("rating",flat=True,
        ).filter( vendor=obj.id)
        return rating
    def get_reviews(self, obj):
        description = models.VendorsReview.objects.values_list("description",
        flat=True).filter( vendor=obj.id)
        return description
    
    def get_priject_images(self, obj):
        priject_images = models.Services.objects.filter(vendor_id=obj.id).values_list("service_image",flat=True)
        return priject_images
    
    def get_user_image(self, obj):
        user_images = models.CustomUser.objects.filter(id=obj.id).values_list("profile_picture",flat=True)
        return user_images
    
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
