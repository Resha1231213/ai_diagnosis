from django.contrib import admin
from django.urls import path
from diagnosis.views import submit_request  # <-- добавить

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', submit_request, name='submit_request'),  # <-- это твоя форма на главной
]