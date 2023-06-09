from django.contrib import admin
from django.contrib.auth import get_user_model
from authemail.admin import EmailUserAdmin
# Register your models here.
class UserAdmin(EmailUserAdmin):
    fieldsets=(
        ('None',{'fields':('email','password')}),
        ('Personal info',{'fields':('first_name','last_name')}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions','is_verified')}),
        ('Important dates',{'fields':('last_login','date_joined')}),
        ('Custom Info',{'fields':('phone',)}),
    )
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(),UserAdmin)
