from rest_framework import serializers
from . import models
from rest_framework.response import Response
from django.db.models import F,FloatField ,Sum ,Avg





class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields ='__all__'

class OrderCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CreateCart
        fields ='__all__'


class postOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields ='__all__'
        

    
class OrderSerializer(serializers.ModelSerializer):
    event_details=serializers.SerializerMethodField()
    package_details=serializers.SerializerMethodField()
    # subamount=serializers.SerializerMethodField()
    # total_amount=serializers.SerializerMethodField()
    class Meta:
        model = models.Order
        fields =['user',
                 'order_Type',
                 'order_status',
                 'delivery_address',
                 'order_create',
                 'Vendor',
                 'event_details',
                 'package_details',
                ]
    def get_event_details(self,obj):
        event_details=models.Events.objects.filter(Vendor=obj.Vendor)
        return str(event_details)
    
    def get_package_details(self,obj):
        package_details=models.Packages.objects.filter(vendors=obj.Vendor)
        return str(package_details)
    
    

    # def get_subamount(self,obj):
    #     return models.CreateCart.objects.filter(cart__cartID=obj.user).aggregate(
    #         total=Sum(F('prodcut_amount')*F('product_quantity'),output_field=FloatField()))["total"]

    # def get_total_amount(self,obj):
    #     return models.Order.objects.filter(Vendor=obj.Vendor).aggregate(
    #         total=Sum(F('taxes')+F('total_amount'),output_field=FloatField()))["total"]

class DetailsSerializers(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    Categorie = serializers.SerializerMethodField()
    class Meta:
        model = models.Vendors
        fields =['id','image','name','Categorie','rating']
    def get_rating(self,obj):
        rating=models.VendorsReview.objects.filter(vendor=obj).values_list("rating",flat=True)
        return rating
    def get_Categorie(self,obj):
        Categorie=models.Categories.objects.filter(name=obj.categories.name).values_list("name",flat=True)
        return Categorie
class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Categories
        fields =['id','image','name']
        
        
class PackagesSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = models.Packages
        fields = "__all__"
        
    def get_image(self, obj):
        image = models.ImageList.objects.filter(vendor_id=obj).values_list("image",flat=True)
        return image

class VendorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Vendors
        fields = "__all__"

class VendorsTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Vendors
        fields = ["id","image","name",]

class ServicesSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Services
        fields = "__all__"
############-----------------------------------
class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['event_title','event_type','event_date','event_time','event_location','total_amount']
#######-----------------------------

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
    project_images=serializers.SerializerMethodField()
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
    
    def get_project_images(self, obj):
        project_images = models.ImageList.objects.filter(vendor_id=obj).values_list("image",flat=True)
        return project_images
    
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
        fields =['id','room','room_type']
   
class RoomPostSerializer(serializers.ModelSerializer):
     class Meta:
        model = models.Room
        fields =['room','room_type','subscribers',]
