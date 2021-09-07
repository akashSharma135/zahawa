from django.urls import path

from . import views



urlpatterns = [
    path("event_types/", views.EventsTypeView.as_view()),
    path("room/", views.RoomView.as_view()),
    path("Vendor/", views.VendorListView.as_view()),
    path("Vendor/service/", views.VendorServiceView.as_view()),
    path("Vendor/review/", views.VendorReviewView.as_view()),
    path("Propsal/search/", views.PropsalView.as_view()),
    path("services/", views.ServiceListView.as_view()),
    path("search/", views.ApiSearchView.as_view()),
    path("profile/loyaltyprogram/Search/", views.loyaltySearchView.as_view()),
    path("categories/", views.CategoriesView.as_view()),
    path("categories/details/<int:pk>/", views.CategoriesDetailsView.as_view()),
    path("vendor_type/", views.VendorTypeView.as_view()),
    # path("OrderDetails/", views.OrderDetailsView.as_view()),
    path("OrderSearch/", views.OrderSearchView.as_view()),
    # path("UserOrder/<int:pk>/", views.UserOrderDView.as_view()),
    path("UserOrder/", views.UserOrderView.as_view()),
    path("Cart/", views.UserCartView.as_view()),
    path("MyCart/", views.MyCartView.as_view()),
    path("MyCart/<int:pk>/", views.MyCartView.as_view()),
    path("TeamView/<int:pk>/", views.TeamView.as_view()),
    path("service_package_deatils/", views.ServicePackageView.as_view()),
    
]
