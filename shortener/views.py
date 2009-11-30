import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect,HttpResponseForbidden,HttpResponseBadRequest

from django.utils import simplejson
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.db import transaction
from django.conf import settings

from urlweb.shortener.baseconv import base62
from urlweb.shortener.models import Link, LinkSubmitForm, Stat,UserProfile
from django.contrib.auth.models import User

def follow(request, base62_id, stat_type = 1):
    """ 
    View which gets the link for the given base62_id value
    and redirects to it.
    """
    import datetime
    
    key = base62.to_decimal(base62_id)
    link = get_object_or_404(Link, pk = key)
    if request.user.is_anonymous():
        user = User.objects.get(username="admin")
    else:
        user = request.user
        
    if str(stat_type) == "v":
        stat_type = 2 
    else:
        stat_type = 1
        
    stat = Stat(
        link = link,
        http_host       = request.META.get("HTTP_HOST",""),      
        http_referer    = request.META.get("HTTP_REFERER",""),   
        http_user_agent = request.META.get("HTTP_USER_AGENT",""),
        remote_addr     = request.META.get("REMOTE_ADDR",""),  
        remote_host     = request.META.get("REMOTE_HOST",""),
        stat_type       = stat_type,
        date            = datetime.datetime.now()
    )
    stat.user = user
    stat.save()
    return HttpResponsePermanentRedirect(link.url)

def default_values(request, link_form=None):
    """ 
    Return a new object with the default values that are typically
    returned in a request.
    """
    if not link_form:
        link_form = LinkSubmitForm()
    allowed_to_submit = is_allowed_to_submit(request)
    return { 'show_bookmarklet': allowed_to_submit,
             'show_url_form': allowed_to_submit,
             'site_name': settings.SITE_NAME,
             'site_base_url': settings.SITE_BASE_URL,
             'link_form': link_form,
             }

def info(request, base62_id):
    """
    View which shows information on a particular link
    """
    key = base62.to_decimal(base62_id)
    link = get_object_or_404(Link, pk = key)
    values = default_values(request)
    values['link'] = link
    return render_to_response(
        'shortener/link_info.html',
        values,
        context_instance=RequestContext(request))

def submit(request):
    """
    View for submitting a URL
    """
    if settings.REQUIRE_LOGIN and not request.user.is_authenticated():
        # TODO redirect to an error page
        raise Http404
    url = None
    link_form = None
    if request.GET:
        link_form = LinkSubmitForm(request.GET)
    elif request.POST:
        link_form = LinkSubmitForm(request.POST)
    if link_form and link_form.is_valid():
        url = link_form.cleaned_data['u']
        link = Link.objects.create_link(url, request.user)
        values = default_values(request)
        values['link'] = link
        return render_to_response(
            'shortener/submit_success.html',
            values,
            context_instance=RequestContext(request))
    values = default_values(request, link_form=link_form)
    return render_to_response(
        'shortener/submit_failed.html',
        values,
        context_instance=RequestContext(request))
        
def user(request,user_id = None, username =  None):
    user = get_object_or_404(User, pk = user_id)
    
    values = default_values(request)
    
    values["links"] = user.link_set.all().order_by("-date_submitted")
    values["user"]  = user
    
    return render_to_response(
        'shortener/user/main.html',
        values,
        context_instance=RequestContext(request))

def index(request):
    """
    View for main page (lists recent and popular links)
    """
    values = default_values(request)
    values['recent_links'] = Link.objects.all().order_by('-date_submitted')[0:10]
    #values['most_popular_links'] = Link.objects.all().order_by('-usage_count')[0:10]
    return render_to_response(
        'shortener/index.html',
        values,
        context_instance=RequestContext(request))

def is_allowed_to_submit(request):
    """
    Return true if user is allowed to submit URLs
    """
    return not settings.REQUIRE_LOGIN or request.user.is_authenticated()

def shorten(request,url = None):
    from django.utils import simplejson as json
    
    url =  request.GET.get("url", None)
    api_key = request.GET.get("api_key", None)
    if not url:
        return HttpResponseBadRequest("you need to submit a url for shortening")
        
    
    
    logging.debug("url: %s api key: %s " % (url, api_key) )
    if not api_key:
        return HttpResponseBadRequest("you need to submit an api key. Example ?api_key=aaaaaaaaaaaaaa")
        
    try:
        user_p = UserProfile.objects.get(api_key=api_key)
    except:
        return HttpResponseBadRequest("No user matching your api_key")
        

    link = Link.objects.create_link(url, user_p.user)
    
    json = json.dumps(link.short_url())
    
    callback = request.GET.get("callback", None)
    if callback:
        json = callback + "("+json+");"
    return HttpResponse(json,content_type="text/javascript")

