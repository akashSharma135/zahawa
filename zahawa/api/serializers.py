from rest_framework import serializers
from . import models
from django.db.models import Avg



class VendorsReviewserializer(serializers.ModelSerializer):
    user_image= serializers.SerializerMethodField()
    class Meta:
        model = models.VendorsReview
        fields = "__all__"
        
    def get_user_image(self, obj):
        image = models.CustomUser.objects.filter(profile_picture=obj.user.id)
        return image

class ServiceSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    class Meta:
        model = models.Services
        fields = "__all__"
    def get_rating(self, obj):
        rating = models.VendorsReview.objects.filter(vendor=obj.id).aggregate(
            Avg("rating")
        )
        return str(rating["rating__avg"])

class VendorListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = models.Vendors
        fields = "__all__"
    def get_avg_rating(self, obj):
        avg_rating = models.VendorsReview.objects.filter(vendor=obj.id).aggregate(
            Avg("avg_rating")
        )
        return str(avg_rating["rating__avg"])
    
    # def get_rating(self, obj):
    #     rating = models.VendorsReview.objects.filter(vendor=obj.id).values("rating")
    #     return rating
    
    
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
