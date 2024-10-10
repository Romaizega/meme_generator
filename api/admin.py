from django.contrib import admin

from api.models import Meme, MemeTemplate, Rating, MemeUser


class MemeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'bottom_text',
        'created_by',
        'created_at',
    )

class RatingAdmin(admin.ModelAdmin):
    pass

class MemeUserAdmin(admin.ModelAdmin):
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
admin.site.register(MemeUser, MemeUserAdmin)
admin.site.register(Meme, MemeAdmin)
