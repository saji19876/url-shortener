from django.contrib import admin

<<<<<<< HEAD
from urlweb.shortener.models import Link,Stat,UserProfile
=======
from urlweb.shortener.models import Link
>>>>>>> 8447a4f298bf1eb8bbeb5df2011adda9e86aabe4

class LinkAdmin(admin.ModelAdmin):
    model = Link
    extra = 3
<<<<<<< HEAD
    
class StatAdmin(admin.ModelAdmin):
    model = Stat
    extra = 3
    
    
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile

admin.site.register(Stat, StatAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
=======

admin.site.register(Link, LinkAdmin)
>>>>>>> 8447a4f298bf1eb8bbeb5df2011adda9e86aabe4
