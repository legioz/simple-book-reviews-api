from __future__ import annotations
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from . import managers


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    is_deleted = models.BooleanField("Deleted", default=False, blank=False, null=False)
    is_active = models.BooleanField("Active", default=True, blank=False, null=False)
    is_staff = models.BooleanField("Staff", default=False, blank=False, null=False)
    is_superuser = models.BooleanField(
        "Superuser", default=False, blank=False, null=False
    )
    login_attempts = models.IntegerField(
        "Total Login Attempts", blank=False, null=False, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = None
    objects = managers.UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "01 - User"

    def __str__(self) -> str:
        return f"{self.email}"

    def get_username(self) -> str:
        return self.email

    def delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def update(self, commit=False, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if commit:
            self.save()

    def set_login_attempt(self):
        self.login_attempts += 1
        self.save()

    def reset_login_attempts(self):
        self.login_attempts = 0
        self.save()


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    book_id = models.IntegerField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "01 - User"

    def __str__(self) -> str:
        return f"{self.user}|{self.book_id}"
