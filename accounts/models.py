from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"
        ADMIN = "admin", "Administrator"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    course = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser and self.role == self.Role.STUDENT:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)
