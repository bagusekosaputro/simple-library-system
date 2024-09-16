from django.db import models

# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=254)
    author  = models.CharField(max_length=254)
    copies = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey("auth.User", related_name="books_created_by", on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey("auth.User", related_name="books_updated_by", on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"], name="books_title_idx"),
            models.Index(fields=["author"], name="books_author_idx"),
            models.Index(fields=["copies"], name="books_copies_idx"),
            models.Index(fields=["available"], name="books_available_idx"),
        ]