from django.db import models

from library_system.books.models import Books


# Create your models here.
class BorrowedBooks(models.Model):
    student_id = models.ForeignKey("auth.User", related_name="borrowed_books_student_id", on_delete=models.DO_NOTHING)
    book_id = models.ForeignKey(Books, related_name="borrowed_books_book_id", on_delete=models.DO_NOTHING)
    borrowed_date = models.DateTimeField()
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(blank=True, null=True)
    renewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey("auth.User", related_name="borrowed_books_created_by", on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey("auth.User", related_name="borrowed_books_updated_by", on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["borrowed_date"], name="bbooks_borrowed_date_idx"),
            models.Index(fields=["due_date"], name="bbooks_books_due_date_idx"),
            models.Index(fields=["returned_date"], name="bbooks_returned_date_idx"),
            models.Index(fields=["renewed"], name="bboks_renewed_idx"),
        ]