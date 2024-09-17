from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from library_system.books.models import Books
from library_system.books.permissions import AuthorAllReadOnlyExceptStaff
from library_system.books.serializers import BookInfoSerializer, BookAddSerializer, BookBorrowOrReturnSerializer, \
    BookUpdateSerializer
from library_system.students.models import Students
from library_system.students.serializers import StudentSerializer


class BookList(APIView):
    permission_classes = [AuthorAllReadOnlyExceptStaff]

    def get(self, request, format=None):
        books = Books.objects.all()
        serializer = BookInfoSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        data["created_by"] = request.user.id
        serializer = BookAddSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

class BookDetail(APIView):
    permission_classes = [AuthorAllReadOnlyExceptStaff]

    def get(self, request, pk):
        try:
            book = Books.objects.get(pk=pk)
            serializer = BookInfoSerializer(book)
            return JsonResponse(serializer.data, safe=True)
        except Books.DoesNotExist:
            raise Http404


    def put(self, request, pk):
        try:
            book = Books.objects.get(pk=pk)
            req_data = JSONParser().parse(request)
            serializer = BookUpdateSerializer(data=req_data)
            if serializer.is_valid():
                user = User.objects.get(email=serializer.data["email"])
                student = self.__get_or_create_student(user, request.user.id)
                if serializer.data["operation"] == "borrow":
                    data = {
                        "borrowed_date": datetime.now().strftime("%Y-%m-%d"),
                        "due_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                        "book_id": book.id,
                        "student_id": user.id,
                        "created_by": request.user.id
                    }
                else:
                    data = {
                        "returned_date": datetime.now().strftime("%Y-%m-%d"),
                    }
                detail_serializer = BookBorrowOrReturnSerializer(data=data)
                if detail_serializer.is_valid():
                    detail_serializer.save()

                    new_copies = (book.copies - 1) if book.copies > 0 else 0
                    book_update_data = {
                        "copies": new_copies,
                        "available": True if new_copies > 0 else False,
                        "updated_by": request.user.id,
                        "updated_at": datetime.now()
                    }
                    student_update_data = {
                        "updated_by": request.user.id,
                        "updated_at": datetime.now(),
                        "book_quota": (student.book_quota - 1) if student.book_quota > 0 else 0
                    }
                    self.__process_update_book(book_update_data, book)
                    self.__process_update_student(student_update_data, student)
                    return JsonResponse(detail_serializer.data, safe=True)

                return HttpResponse(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Books.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        try:
            book = Books.objects.get(pk=pk)
            data = JSONParser().parse(request)
            data["updated_by"] = request.user.id
            data["updated_at"] = datetime.now()
            serializer = BookAddSerializer(book, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)

            return JsonResponse(serializer.errors, status=400)
        except Books.DoesNotExist:
            raise Http404

    def __process_update_book(self, data, book):
        book_serializer = BookInfoSerializer(book, data=data, partial=True)
        if book_serializer.is_valid():
            book_serializer.save()

        return book_serializer.data

    def __process_update_student(self, data, student):
        student_serializer = StudentSerializer(student, data=data, partial=True)
        if student_serializer.is_valid():
            student_serializer.save()

        return student_serializer.data

    def __get_or_create_student(self, user, created_by):
        try:
            student = Students.objects.get(user_id=user.id)
            return student
        except Students.DoesNotExist:
            data = {
                "name": " ".join([user.first_name, user.last_name]),
                "user_id": user.id,
                "created_by": created_by
            }
            student_serializer = StudentSerializer(data=data)
            if student_serializer.is_valid():
                student_serializer.save()

            return student_serializer.data