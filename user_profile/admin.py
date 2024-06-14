from django.contrib import admin

from user_profile.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'avatar')
    search_fields = ('username', "email")
    list_filter = ('is_staff',)


admin.site.register(User, UserAdmin)
