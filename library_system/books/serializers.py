from rest_framework import serializers

from library_system.books.models import Books


class BookSerializer(serializers.Serializer):
    class Meta:
        model = Books
        fields = ["id", "title", "author", "copies", "available"]
