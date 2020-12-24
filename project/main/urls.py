from django.contrib import admin
from django.urls import path, include

api_urlpatterns = [
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]
