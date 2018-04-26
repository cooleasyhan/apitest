from django.conf.urls import url, include
from .views import APITestView
from rest_framework import routers
router = routers.DefaultRouter()

urlpatterns = [
    url(r'^testapi/$', APITestView.as_view()),
    url(r'^api/', include(router.urls)),
]
