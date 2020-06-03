from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_superuser(self, email, first_name=None, last_name=None, password=None):
        user = User(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create(self, email, first_name=None, last_name=None, password=None):
        user = User(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = UserManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
