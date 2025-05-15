from django.contrib import admin
from django.urls import path
from diagnosis.views import submit_request, result_view, premium_result_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', submit_request, name='submit'),
    path('result/', result_view, name='result'),
    path('premium/', premium_result_view, name='premium_result'),
]
