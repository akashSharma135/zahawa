from django.db import models
from users.models import CustomUser
# Create your models here.




class Image(models.Model):
    models.ImageField(
        upload_to=None, null=True, blank=True, default="media/None/default.png"
    )
    
ROOM_CHOICES= (
    ("users","users"),
    ("groups","groups"),
    ("team","team"),
    ("game","game"),
    ("tournament","tournament"),
    ("streaming","streaming")
)
class Room(models.Model):
    name = models.CharField(blank=True, null=True, max_length=100)
    subscribers=models.ManyToManyField(CustomUser)
    room_type = models.CharField(max_length=20, choices=ROOM_CHOICES, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
ORDER_CHOICES= (
    ("Active","Active"),
    ("Completed","Completed"),  
)
STATUS_CHOICES= (
    ("Order_Placed","Order_Placed"),
    ("Confirmed","Confirmed"),
    ("On Process","On Process"),
    ("Completed","Completed"),
    ("Cancelled","Cancelled"),
)
class Order(models.Model):
    # order
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_Type=models.CharField(max_length=20, choices=ORDER_CHOICES, null=True)
    order_status=models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    order_datetime=models.DateTimeField(blank=True, null=True, max_length=100)
    
    
    
    event_title=models.CharField(blank=True, null=True, max_length=100)
    event_type=models.CharField(blank=True, null=True, max_length=100)
    event_date=models.DateField(blank=True, null=True, max_length=100)
    event_time=models.TimeField()
    event_location=models.CharField(blank=True, null=True, max_length=100)
    delivery_address=models.CharField(blank=True, null=True, max_length=100)
    total_amount=models.PositiveIntegerField(default=0,blank=True)
    taxes=models.PositiveIntegerField(default=0,blank=True)
    # grand_total=models.PositiveIntegerField()
           
class Vendors(models.Model):
    # user_id
    name =models.CharField(blank=True, null=True, max_length=100)
    image =models.ImageField(
         null=True, blank=True, default="media/None/default.png"
    )
    location =models.CharField(blank=True, null=True, max_length=100)
    city=models.CharField(blank=True, null=True, max_length=100)
    # vendor_category
    description=models.TextField(blank=True, null=True, max_length=400)
    is_favorite=models.BooleanField(default=False,null=True,blank=True)
    
    project_gallery=models.ForeignKey(Image,
         null=True, blank=True, default="media/None/default.png",
    on_delete=models.CASCADE) #manytomany
    package_type=models.CharField(blank=True, null=True, max_length=100)
    product_name=models.CharField(blank=True, null=True, max_length=100)
    prodcut_amount=models.PositiveIntegerField(default=0)
    item_quantity=models.PositiveIntegerField(default=0)
    previous_work_Description=models.TextField(blank=True, null=True, max_length=400)
    ratings=models.IntegerField(blank=True, null=True, max_length=100)
    reviews=models.CharField(blank=True, null=True, max_length=100)  #textfield

class Services(models.Model):
    vendor_id=models.ForeignKey(Vendors, on_delete=models.CASCADE)
    service_name=models.CharField(blank=True, null=True, max_length=100)
    service_image= models.ImageField(
        upload_to=None, null=True, blank=True)
    
    service_minAmount=models.PositiveIntegerField(default=0 )
    service_maxAmount=models.PositiveIntegerField(default=0)
    rating=models.IntegerField(default=0,blank=True)
    review=models.TextField(blank=True, null=True)

class ChatList(models.Model):
    user  =models.ForeignKey(CustomUser,blank=True, null=True,on_delete=models.CASCADE)
    vendor=models.ForeignKey(Vendors,blank=True, null=True,on_delete=models.CASCADE)
    last_message=models.CharField(blank=True, null=True, max_length=100)
    last_messageDate=models.DateField(blank=True, null=True, max_length=100)

class Cart(models.Model):
    cartID=models.ForeignKey(CustomUser,blank=True, null=True,on_delete=models.CASCADE)
    cart_createdDate=models.DateField(blank=True, null=True, max_length=100)
    cart_createdTime=models.TimeField()
    
class Member(models.Model):
    members=models.ForeignKey(CustomUser,blank=True, null=True,on_delete=models.CASCADE)
    # profile_picture = models.ImageField(
    #     upload_to=None, null=True, blank=True, default="media/None/default.png"
    # )
    captain=models.CharField(blank=True, null=True, max_length=100)
    vice_captain=models.CharField(blank=True, null=True, max_length=100)
    create=models.DateTimeField(auto_now=True,blank=True, null=True, max_length=100)

    
class Team(models.Model):
    thumb=models.ImageField(
        upload_to=None, null=True, blank=True, default="media/None/default.png"
    )
    name=models.CharField(blank=True, null=True, max_length=100)
    members=models.ManyToManyField(Member)
    rank=models.PositiveIntegerField(default=0,blank=True)
    created=models.DateTimeField(auto_now=True,blank=True)
    
