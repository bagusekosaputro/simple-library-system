from rest_framework import serializers

from library_system.books.models import Books
from library_system.borrowed_books.models import BorrowedBooks


OPERATION_CHOICES = ["borrow", "return"]

class BorrowedBookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = ["borrowed_date", "due_date"]

class BookInfoSerializer(serializers.ModelSerializer):
    details = BorrowedBookInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Books
        fields = ["id", "title", "author", "copies", "available", "details"]



class BookAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ["id", "title", "author", "copies", "available", "created_by", "updated_at", "updated_by"]


class BookBorrowOrReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = ["borrowed_date", "due_date", "renewed", "created_by", "updated_at", "updated_by", "book_id", "student_id"]


class BookUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    operation = serializers.ChoiceField(choices=OPERATION_CHOICES)
    renewed = serializers.BooleanField(default=False)
