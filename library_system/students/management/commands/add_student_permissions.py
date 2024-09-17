from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from library_system.students.models import Students


class Command(BaseCommand):
    help = "Create user groups and add permissions for students"

    def handle(self, *args, **options):
        student_group, created = Group.objects.get_or_create(name="Student")
        librarian_group, created = Group.objects.get_or_create(name="Librarian")
        admin_group, created = Group.objects.get_or_create(name="Admin")

        content_type = ContentType.objects.get_for_model(Students)
        permissions = Permission.objects.filter(content_type=content_type)
        print([perm.codename for perm in permissions])
        admin_permissions = [
            f"add_{Students.__name__.lower()}",
            f"change_{Students.__name__.lower()}",
            f"delete_{Students.__name__.lower()}",
            f"view_{Students.__name__.lower()}"
        ]

        librarian_permissions = [
            f"change_{Students.__name__.lower()}",
            f"view_{Students.__name__.lower()}"
        ]
        student_permissions = [
            f"view_{Students.__name__.lower()}"
        ]

        # for perm in permissions:
        #     if perm.codename in admin_permissions:
        #         admin_group.permissions.add(perm)
        #
        #     if perm.codename in librarian_permissions:
        #         librarian_group.permissions.add(perm)
        #
        #     if perm.codename in student_permissions:
        #         student_group.permissions.add(perm)