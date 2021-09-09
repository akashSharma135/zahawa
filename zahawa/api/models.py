from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.





ROOM_CHOICES = (
    ("users", "users"),
    ("groups", "groups"),
    ("team", "team"),
    ("game", "game"),
    ("tournament", "tournament"),
    ("streaming", "streaming"),
)


class Room(models.Model):
    room = models.CharField(blank=True, null=True, max_length=100)
    subscribers=models.JSONField(blank=True, null=True,default=[], max_length=400)
    room_type = models.CharField(max_length=20, choices=ROOM_CHOICES, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


ORDER_CHOICES = (
    ("Active", "Active"),
    ("Completed", "Completed"),
)
STATUS_CHOICES = (
    ("Order_Placed", "Order_Placed"),
    ("Confirmed", "Confirmed"),
    ("On Process", "On Process"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
)





RESTRICTION_CHOICES = (
    ("invite", "invite"),
    ("subscriber", "subscriber"),
    ("team", "team"),
    ("all", "all"),
)





class Categories(models.Model):
    name = models.CharField(blank=True, null=True, max_length=100)
    image=models.ImageField(upload_to=None, null=True, blank=True,default="media/default.png")

    


class Vendors(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(blank=True, null=True, max_length=100)
    image = models.ImageField(null=True, blank=True, default="media/default.png")
    description = models.TextField(blank=True, null=True, max_length=400)
    is_favorite = models.BooleanField(default=False, null=True, blank=True)
    categories=models.ForeignKey(Categories,null=True,blank=True, on_delete=models.CASCADE)
    #Products=models.ForeignKey(Product,null=True,blank=True, on_delete=models.CASCADE)
    #Package=models.ForeignKey(Packages,null=True,blank=True, on_delete=models.CASCADE)
    #Service=models.ForeignKey(Services,null=True,blank=True, on_delete=models.CASCADE)
    # project_gallery = models.ForeignKey(
    #     Image,
    #     null=True,
    #     blank=True,
    #     default="media/default.png",
    #     on_delete=models.CASCADE,
    # )


    
class ImageList(models.Model):
    image=models.ImageField(
        upload_to=None, null=True, blank=True, default="media/default.png"
    )
    vendor_id=models.ForeignKey(Vendors,null=True,blank=True,on_delete=models.CASCADE)

class VendorsReview(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    description = models.CharField(max_length=250, null=True, blank=True)#change to review

class Services(models.Model):
    vendors=models.ForeignKey(Vendors,null=True,blank=True, on_delete=models.CASCADE)
    service_name = models.CharField(blank=True, null=True, max_length=100)
    service_image = models.ImageField(upload_to=None, null=True, blank=True)

    service_minAmount = models.PositiveIntegerField(default=0)
    service_maxAmount = models.PositiveIntegerField(default=0)
class ServicesReview(models.Model):
    services = models.ForeignKey(Services, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    description = models.CharField(max_length=250, null=True, blank=True)


class ChatList(models.Model):
    user = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.CASCADE
    )
    vendor = models.ForeignKey(Vendors, blank=True, null=True, on_delete=models.CASCADE)
    last_message = models.CharField(blank=True, null=True, max_length=100)
    last_messageDate = models.DateField(blank=True, null=True, max_length=100)


    



class Product(models.Model):
    vendors=models.ForeignKey(Vendors,null=True,blank=True, on_delete=models.CASCADE)
    product_name=models.CharField(blank=True, null=True, max_length=100)
    product_type=models.CharField(null=True, max_length=100)
    prodcut_amount=models.PositiveIntegerField(default=0)
    #product_quantity=models.PositiveIntegerField(default=1)  


class Packages(models.Model):
    vendors=models.ForeignKey(Vendors,null=True,blank=True, on_delete=models.CASCADE)
    packages_type=models.CharField(blank=True, null=True, max_length=100)
    duration=models.TimeField(auto_now_add=False,blank=True, null=True)
    amount=models.PositiveIntegerField(default=0, blank=True)
    image = models.ImageField(null=True, blank=True, default="media/default.png")
    

class Events(models.Model):
    event_title = models.CharField(blank=True, null=True, max_length=100)
    event_image = models.ImageField(null=True, blank=True, default="media/default.png")
    event_type = models.CharField(blank=True, null=True, max_length=100)
    event_date = models.DateField(blank=True, null=True, max_length=100)
    event_time = models.TimeField(auto_now_add=False,blank=True, null=True)
    event_location = models.CharField(blank=True, null=True, max_length=100)
    Packages = models.ForeignKey(Packages,blank=True, null=True, on_delete=models.CASCADE)
    # Vendor=models.ForeignKey(Vendors,null=True,blank=True, on_delete=models.CASCADE)

  
class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.CASCADE
    )
    cart_createdDate = models.DateField(auto_now_add=False,blank=True, null=True)
    cart_createdTime = models.TimeField(auto_now_add=True,blank=True, null=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, blank=True, null=True, on_delete=models.CASCADE)
    # order = models.ForeignKey(
    #     Order,null=True, on_delete=models.CASCADE)
    Packages = models.ForeignKey(Packages,blank=True, null=True, on_delete=models.CASCADE)
    # Packages_quantity=models.PositiveIntegerField(default=1)  
    Product = models.ForeignKey(Product, blank=True, null=True,on_delete=models.CASCADE)
    Product_quantity=models.PositiveIntegerField(default=1)  
    prodcut_amount=models.PositiveIntegerField(default=0)
    
class Order(models.Model):
    # order
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_Type = models.CharField(max_length=20, choices=ORDER_CHOICES, null=True)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    Cart=models.ForeignKey(CartItem, null=True,on_delete=models.CASCADE)
    # Vendor =models.ForeignKey(Vendors, null=True,on_delete=models.CASCADE)
    delivery_address = models.CharField(blank=True, null=True, max_length=100)
    #total_amount = models.PositiveIntegerField(default=0, blank=True)
    #taxes = models.PositiveIntegerField(default=0, blank=True)
    order_create = models.DateTimeField(auto_now=True,blank=True, null=True)
    # grand_total=models.PositiveIntegerField()
    # Packages = models.ForeignKey(Packages,blank=True, null=True, on_delete=models.CASCADE)
    # Packages_quantity=models.PositiveIntegerField(default=1)  
    # Product = models.ForeignKey(Product, blank=True, null=True,on_delete=models.CASCADE)
    # Product_quantity=models.PositiveIntegerField(default=1)  
    




class Team(models.Model):
    thumb = models.ImageField(
        upload_to=None, null=True, blank=True, default="media/default.png"
    )
    name = models.CharField(blank=True, null=True, max_length=100)
    
class Member(models.Model):
    members = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.CASCADE
    )
    profile_picture = models.ImageField(
        upload_to=None, null=True, blank=True, default="media/None/default.png"
    )
    captain = models.CharField(blank=True, null=True, max_length=100)
    vice_captain = models.CharField(blank=True, null=True, max_length=100)
    team = models.ForeignKey(
        Team, blank=True, null=True, on_delete=models.CASCADE
    )
    create = models.DateTimeField(auto_now_add=True, blank=True, null=True)


Proposals_STATUS= (
    
    ("Submitted", "Submitted"),
    ("Offered", "Offered"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
    
    
)

class Proposals(models.Model):
    user = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.CASCADE
    )
    Proposals_status = models.CharField(max_length=20, choices=Proposals_STATUS, null=True)
    Proposals_type = models.CharField(max_length=20, choices=Proposals_STATUS, null=True)
    title = models.TextField(blank=True, null=True, max_length=400)
    created = models.DateTimeField(auto_now_add=False,blank=True, null=True)
    
