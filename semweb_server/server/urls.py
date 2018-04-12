from django.conf.urls import url
from server import views

urlpatterns = [
    url(r'^(?P<country>[A-Z]{2})/$', views.fetch_country)
]



