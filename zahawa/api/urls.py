from django.urls import path

from . import views



urlpatterns = [
    path("event_types", views.EventsTypeView.as_view()),
    path("room/", views.RoomView.as_view()),
    path("Vendor/", views.VendorListView.as_view()),
    path("Vendor/service/", views.VendorServiceView.as_view()),
    path("Vendor/review/", views.VendorReviewView.as_view()),
]

