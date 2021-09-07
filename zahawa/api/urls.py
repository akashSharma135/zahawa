from django.urls import path

from . import views



urlpatterns = [
    path("event_types/", views.EventsTypeView.as_view()),
    path("room/", views.RoomView.as_view()),
    path("vendor/", views.VendorListView.as_view()),
    path("vendor/service/", views.VendorServiceView.as_view()),
    path("vendor/review/", views.VendorReviewView.as_view()),
    path("propsal/search/", views.PropsalView.as_view()),
    path("services/", views.ServiceListView.as_view()),
    path("search/", views.ApiSearchView.as_view()),
    path("profile/loyaltyprogram/Search/", views.loyaltySearchView.as_view()),
    path("categories/", views.CategoriesView.as_view()),
    path("categories/details/<int:pk>/", views.CategoriesDetailsView.as_view()),
    path("vendor_type/", views.VendorTypeView.as_view()),
    # path("OrderDetails/", views.OrderDetailsView.as_view()),
    path("orderSearch/", views.OrderSearchView.as_view()),
    # path("UserOrder/<int:pk>/", views.UserOrderDView.as_view()),
    path("userOrder/", views.UserOrderView.as_view()),
    path("cart/", views.UserCartView.as_view()),
    path("my_cart/", views.MyCartView.as_view()),
    path("my_cart/<int:pk>/", views.MyCartView.as_view()),
    path("team_view/<int:pk>/", views.TeamView.as_view()),

]

