from django.urls import path

from . import views



urlpatterns = [
    path("event_types", views.EventsTypeView.as_view(), name="request_list"),
    path("event_types", views.EventsTypeView.as_view(), name="request_list"),

]
