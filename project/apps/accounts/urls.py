from django.urls import include, path
from rest_framework import routers

from apps.accounts import views

router = routers.SimpleRouter()
router.register(r'', views.UserViewSet)

app_name = 'accounts'

urlpatterns = [
    path('', include(router.urls)),
]
