from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver


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
    
    def __str__(self):
        return self.email


class City(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    nick = models.CharField(
        max_length=4, 
        null=True,
        blank=True,
        unique=True
        )

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
        City,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="İl"
        )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="İlçe"
        )
    neighborhood = models.ForeignKey(
        Neighborhood,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Mahalle"
        )
    extra_info = models.TextField(
        max_length=255,
        verbose_name="Sokak-Apartman"
        )

    def get_full_address(self):
        return f"{self.neighborhood.name} Mahallesi {self.extra_info} {self.district.name}/{self.city.name}"

    def __str__(self):
        return f"{self.district.name.upper()} {self.neighborhood.name.upper()} {self.extra_info.upper()}"

    class Meta:
        ordering = ['id']


class Customer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    nick = models.CharField(
        max_length=9,
        default="",
        unique=True
        )
    phone1 = models.CharField(
        max_length=50,
        verbose_name="Telefon1",
        unique=True
        )
    phone2 = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Telefon2"
        )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        verbose_name="Adres"
        )

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ['user']


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kategori Adı")
    createt_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class DistributionUnitEnum(models.IntegerChoices):
        PIECE = 1, 'Adet'
        LITER = 2, 'Litre'
        KILOGRAM = 3, 'KG'
        KANGAL = 4, 'Kangal'
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Ürün Kategorisi"
        )
    name = models.CharField(max_length=70, verbose_name="Ürün Adı")
    distribution_unit = models.PositiveSmallIntegerField(
        choices=DistributionUnitEnum.choices,
        verbose_name="Dağıtım Birimi"
        )
    price = models.FloatField(verbose_name="Satış Fiyatı")
    purchase_price = models.FloatField(
        verbose_name="Alış Fiyatı",
        )
    createt_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    class Meta:
        ordering = ['category']


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Ürün Adı"
        )
    price = models.FloatField(default=0)
    is_deleted = models.BooleanField(default=False)
    quantity = models.FloatField(
        validators=[MinValueValidator(0.0)],
        verbose_name="Miktar"
        )

    createt_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}\
             quantity: {self.quantity}\
                 {self.product.get_distribution_unit_display()}\
                      price: {self.price} TL"


class Order(models.Model):
    class PaymentMethodEnum(models.IntegerChoices):
        CASH = 1, 'Nakit'
        EFT = 2, 'EFT'

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Müşteri Adı"
        )
    nick = models.CharField(
        max_length=14,
        unique=True
        )
    items = models.ManyToManyField(
        OrderItem,
        verbose_name="Sipariş Ürünleri",
        related_name='order_item'
        )
    delivery_date = models.DateField(verbose_name="Teslimat Tarihi")
    payment_method = models.PositiveSmallIntegerField(
        choices=PaymentMethodEnum.choices,
        blank=True,
        null=True,
        verbose_name="Ödeme Şekli"
    )
    is_delivered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    total_price = models.FloatField(
        validators=[MinValueValidator(0.0)],
        default=0.0,
        verbose_name="Toplam Tutar"
        )
    received_money = models.FloatField(default=0.0)
    remaining_debt = models.FloatField(default=0.0)
    service_fee = models.FloatField(default=0.0)

    is_instagram = models.BooleanField(
        default=False,
        verbose_name="İnstagram?"
        )
    instagram_username = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="İnstagram Adı"
        )
    notes = models.CharField(
        max_length=50,
        verbose_name="Notlar",
        blank=True,
        null=True
        )
    
    createt_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer: {self.customer} - Total: {self.total_price} - Delivered: {self.is_delivered}"

    def total_price_update(self):
        if not self.is_delivered:
            total_price = 0
            for item in self.items.all():
                if item.is_deleted == False:
                    total_price += item.price * item.quantity
                    print("********")
            print(total_price)
            self.total_price = total_price
            self.save()
            print(self.total_price)

    class Meta:
        ordering = ['-delivery_date']


@receiver(post_save, sender=OrderItem)
def order_item_receiver(sender, instance, created, *args, **kwargs):
    if created:
        instance.price = instance.product.price
        instance.save()
    if instance.order_item.last() is not None:
        instance.price = instance.product.price
        instance.order_item.last().total_price_update()


@receiver(m2m_changed, sender=Order.items.through)
def order_receiver(sender, instance, *args, **kwargs):
    print("m2m changed")
    instance.total_price_update()


@receiver(post_save, sender=Product)
def order_item_receiver_for_update(sender, instance, *args, **kwargs):
    for item in instance.orderitem_set.all():
        item.price = instance.price
        item.save()
