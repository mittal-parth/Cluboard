from django.contrib import admin
from accounts.models import Info, Role, Permission, Permission_Assignment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class InfoInLine(admin.StackedInline):
    model = Info
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (InfoInLine,)

# Register your models here.

#Extending the existing User Model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Permission_Assignment)