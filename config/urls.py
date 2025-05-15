from django.contrib import admin
from django.urls import path
from diagnosis.views import submit_request, premium_result

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', submit_request, name='submit_request'),
    path('premium/<int:request_id>/', premium_result, name='premium_result'),
    path('premium/', views.premium_result, name='premium_result'),
]
