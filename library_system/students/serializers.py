from rest_framework import serializers

from library_system.students.models import Students


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ["id", "name", "book_quota", "user_id", "created_by", "updated_by", "updated_at"]