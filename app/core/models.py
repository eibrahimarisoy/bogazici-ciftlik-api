from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    def get_full_name(self):
        """Return the first_name plus last_name, with a space in between"""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name

    def get_short_name(self):
        """Return the first_name plus last_name, with a space in between"""
        return self.first_name


class City(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    nick = models.CharField(max_length=4, null=True, blank=True, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Address(models.Model):
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, verbose_name="İl")
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, verbose_name="İlçe")
    neighborhood = models.ForeignKey(
        Neighborhood, on_delete=models.SET_NULL, null=True, verbose_name="Mahalle")
    extra_info = models.TextField(max_length=255, blank=True, null=True, verbose_name="Sokak-Apartman")

    def get_full_address(self):
        return self.district.name + "-" + self.neighborhood.name + "-" + self.extra_info

    def __str__(self):
        return f"{self.district.name.upper()} {self.neighborhood.name.upper()} {self.extra_info.upper()}"

    class Meta:
        ordering = ['id']