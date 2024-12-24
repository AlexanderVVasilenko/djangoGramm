from django.contrib import admin
from user_profile.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_avatar_url')
    search_fields = ('username', "email")
    list_filter = ('is_staff',)

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else "No Avatar"

    get_avatar_url.short_description = "Avatar URL"


admin.site.register(User, UserAdmin)
