from django.urls import path

from library_system.students import views

urlpatterns = [
    path("students/", views.APIView.as_view())
]