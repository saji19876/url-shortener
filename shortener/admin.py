from django.contrib import admin

from urlweb.shortener.models import Link,Stat,UserProfile


class LinkAdmin(admin.ModelAdmin):
    model = Link
    extra = 3
    
class StatAdmin(admin.ModelAdmin):
    model = Stat
    extra = 3
    
    
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile

admin.site.register(Stat, StatAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

