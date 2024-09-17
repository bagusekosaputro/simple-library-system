from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from library_system.students.models import Students
from library_system.students.serializers import StudentSerializer


# Create your views here.
class StudentList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        books = Students.objects.all()
        serializer = StudentSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)