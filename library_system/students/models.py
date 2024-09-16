from django.db import models

# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=254)
    book_quota = models.PositiveIntegerField(default=10)
    user_id = models.ForeignKey("auth.User", related_name="students_user_id", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey("auth.User", related_name="students_created_by", on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey("auth.User", related_name="students_updated_by", on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"], name="students_name_idx"),
            models.Index(fields=["book_quota"], name="students_book_quota_idx"),
        ]