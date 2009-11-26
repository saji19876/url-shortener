import datetime

from django.db import models
from django.conf import settings
<<<<<<< HEAD
from django.contrib.auth.models import User
from django import forms
from django.db.models.signals import post_save
from urlweb.shortener.baseconv import base62

class UserProfile(models.Model):
     user = models.ForeignKey(User, unique=True)
     api_key = models.CharField(blank=False, max_length=40)
     
def createUserProfile(sender,instance,created, **kwargs):
    import hashlib
    if created:
        api_key = str(hashlib.sha1(str(instance.id) + settings.SECRET_KEY).hexdigest())
        user_profile = UserProfile( user= instance )
        user_profile.api_key = api_key
        user_profile.save()
 
      
post_save.connect(createUserProfile, sender=User)

class LinkManager(models.Manager):
    def create_link(self, url, user = None):
        
        if not user:
            user = User.objects.get(username="admin")
            
        link = None
        try:
            link = self.filter(url = url).filter(main_url = None)
            link = link[0]
        except IndexError:
            link = None
            pass
        if link == None:
            new_link = self.create(url = url,user = user)
            #new_link.save()
            link = new_link
        else:
            new_link = self.create(url = url, main_url= link, user = user)
            #new_link.save()
        link = new_link
        
        return link
=======
#from django.contrib.auth.models import User
from django import forms

from urlweb.shortener.baseconv import base62

>>>>>>> 8447a4f298bf1eb8bbeb5df2011adda9e86aabe4
class Link(models.Model):
    """
    Model that represents a shortened URL

    # Initialize by deleting all Link objects
    >>> Link.objects.all().delete()
    
    # Create some Link objects
    >>> link1 = Link.objects.create(url="http://www.google.com/")
    >>> link2 = Link.objects.create(url="http://www.nileshk.com/")

    # Get base 62 representation of id
    >>> link1.to_base62()
    'B'
    >>> link2.to_base62()
    'C'
    
    # Set SITE_BASE_URL to something specific
    >>> settings.SITE_BASE_URL = 'http://uu4.us/'

    # Get short URL's
    >>> link1.short_url()
    'http://uu4.us/B'
    >>> link2.short_url()
    'http://uu4.us/C'

    # Test usage_count
    >>> link1.usage_count
    0
    >>> link1.usage_count += 1
    >>> link1.usage_count
    1

    """
<<<<<<< HEAD
    user = models.ForeignKey(User)
    url = models.URLField(verify_exists=True, unique=False)
    date_submitted = models.DateTimeField(default=datetime.datetime.now())
    main_url = models.ForeignKey("self",related_name="rollup",blank=True,null=True)
=======
    url = models.URLField(verify_exists=True, unique=True)
    date_submitted = models.DateTimeField(default=datetime.datetime.now())
    usage_count = models.IntegerField(default=0)

>>>>>>> 8447a4f298bf1eb8bbeb5df2011adda9e86aabe4
    def to_base62(self):
        return base62.from_decimal(self.id)

    def short_url(self):
        return settings.SITE_BASE_URL + self.to_base62()
<<<<<<< HEAD
        
    def total_views(self):
        return self.stat_set.filter(stat_type=2).count()
        
    def total_clicks(self):
        return self.stat_set.filter(stat_type=1).count()
    
    def __unicode__(self):
        return self.to_base62() + ' : ' + self.url
        
    objects = LinkManager()
STAT_TYPE_CHOICES = (
    (1,"Click"),
    (2,"View"),
)   
 
class Stat(models.Model):
    link = models.ForeignKey(Link)
    
    http_host       = models.TextField(blank=True)
    http_referer    = models.TextField(blank=True)
    http_user_agent = models.TextField(blank=True)
    remote_addr     = models.TextField(blank=True)
    remote_host     = models.TextField(blank=True)
    date  = models.DateTimeField(default=datetime.datetime.now())
    stat_type = models.IntegerField(default=1, choices=STAT_TYPE_CHOICES)
    
=======
    
    def __unicode__(self):
        return self.to_base62() + ' : ' + self.url

>>>>>>> 8447a4f298bf1eb8bbeb5df2011adda9e86aabe4
class LinkSubmitForm(forms.Form):
    u = forms.URLField(verify_exists=True,
                       label='URL to be shortened:',
                       )
