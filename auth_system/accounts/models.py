from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255, default='abc@gmail.com')
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user/ non superuser
    admin = models.BooleanField(default=False)  # superuser
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name()

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
