from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User, Address, Customer, Product, Category, OrderItem, Order

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['first_name', 'last_name', 'username', 'email']
    fieldsets = (
        (None, {
            'fields': (
                'first_name', 'last_name', 'username'
            ),
        }),
        (('Kişisel Bilgiler'), {'fields': ('email',)}),
        (('İzinler'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (('Önemli Tarihler'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    
admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Order)

