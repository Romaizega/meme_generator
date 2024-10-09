from api.models import MemeTemplate, Rating, User, Meme
from django.contrib import admin



class MemeAdmin(admin.ModelAdmin):
    pass

class RatingAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    pass

class MemeAdmin(admin.ModelAdmin):
    pass

admin.site.register(MemeTemplate, MemeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Meme, MemeAdmin)
