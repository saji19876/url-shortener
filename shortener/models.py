import datetime

from django.db import models
from django.conf import settings
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
    user = models.ForeignKey(User)
    url = models.URLField(verify_exists=True, unique=False)
    title = models.CharField(blank=True, max_length=255)
    trys = models.IntegerField(blank=False, null=True, default=5)
    date_submitted = models.DateTimeField(auto_now_add=True)
    main_url = models.ForeignKey("self",related_name="rollup",blank=True,null=True)
    clicks = models.IntegerField(blank=True, null=True,default=0)
    views = models.IntegerField(blank=True, null=True,default=0) 
    def to_base62(self):
        return base62.from_decimal(self.id)

    def short_url(self):
        return settings.SITE_BASE_URL + self.to_base62()
        
    def total_views(self):
        return self.clicks
        
    def total_clicks(self):
        return self.views
       
    def title_display(self):
        display = ""
        if self.title:
            display = self.title
        else:
            display = self.url     
        return display 
        
    def ctr(self):
        clicks = float(self.clicks)
        views  = float(self.views)
        if views == 0:
            return clicks
            
        return float(clicks / views)

    def ctr_w(self):
        ctr = self.ctr()
        if ctr <= 1:
	    val = ctr * self.views
	else:
	    val = 0

	return val
    
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
    date            = models.DateTimeField(auto_now_add=True)
    stat_type       = models.IntegerField(default=1, choices=STAT_TYPE_CHOICES)
    

class LinkSubmitForm(forms.Form):
    u = forms.URLField(verify_exists=True,
                       label='URL to be shortened:',
                       )
