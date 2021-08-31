from django.urls import path

from . import views



urlpatterns = [
    path("event_types", views.EventsTypeView.as_view()),
    path("room/", views.RoomView.as_view()),
]

