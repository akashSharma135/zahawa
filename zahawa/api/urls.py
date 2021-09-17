from django.urls import path

from . import views



urlpatterns = [
    path("event_types/", views.EventsTypeView.as_view()),
    path("room/", views.RoomView.as_view()),
    path("vendor/", views.VendorListView.as_view()),
    path("vendor/service/<int:pk>/", views.VendorServiceView.as_view()),
    path("vendor/review/<int:pk>/", views.VendorReviewView.as_view()),
    path("propsal/search/", views.PropsalView.as_view()),
    path("propsal/<int:pk>/", views.PropsalUserView.as_view()),
    path("propsal/", views.PropsalUserView.as_view()),
    path("services/", views.ServiceListView.as_view()),
    path("search/", views.ApiSearchView.as_view()),
    path("profile/loyaltyprogram/search/", views.loyaltySearchView.as_view()),
    path("categories/", views.CategoriesView.as_view()),
    path("categories/details/<int:pk>/", views.CategoriesDetailsView.as_view()),
    path("vendor_type/", views.VendorTypeView.as_view()),
    # path("OrderDetails/", views.OrderDetailsView.as_view()),
    path("order_search/", views.OrderSearchView.as_view()),
    # path("UserOrder/<int:pk>/", views.UserOrderDView.as_view()),
    path("user_order/", views.UserOrderView.as_view()),
    path("cart/", views.UserCartView.as_view()),
    path("my_cart/", views.MyCartView.as_view()),
    path("my_cart/<int:pk>/", views.MyCartView.as_view()),
    path("team_view/<int:pk>/", views.TeamView.as_view()),
    path("service_package_deatils/", views.ServicePackageView.as_view()),
    # favourites
    path("favourite_vendor/", views.FavouriteVendorView.as_view()),
    path('favourite_products/', views.FavouriteProductView.as_view()),
    path('favourite_services/', views.FavouriteServiceView.as_view())
]
