from django.conf.urls import include, url
from rest_framework import routers
from rest_framework.authtoken import views

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^api/run$', views.APITestView.as_view()),
    url(r'^api/', include(router.urls)),
    url(r'^api/auth$',views.AuthView.as_view() )
    # url(r'^api-token-auth/', views.obtain_auth_token)
]
