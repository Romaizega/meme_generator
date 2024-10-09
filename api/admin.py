from django.contrib import admin

from api.models import Meme, MemeTemplate, Rating, User


class MemeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'bottom_text',
        'created_by',
        'created_at',
    )

class RatingAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )

class MemeAdmin(admin.ModelAdmin):
    pass

admin.site.register(MemeTemplate, MemeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Meme, MemeAdmin)
