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
from django.db.models import Count
from django.core import serializers

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
        stat_type       = stat_type
    )
    stat.user = user
    stat.save()
    if stat_type == 1:
        link.clicks = link.clicks + 1
    else:
        link.views = link.views + 1
    link.save()
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
    from urlparse import urlparse
    key = base62.to_decimal(base62_id)
    link = get_object_or_404(Link, pk = key)
    values = default_values(request)
    values['link'] = link
    values["stats"] = link.stat_set.all()
    net_locs = dict()
    for stat in values["stats"]:
        if stat.http_referer:
            o = urlparse(stat.http_referer)
            ref = str(o.netloc)
        else:
            ref = "No Referer"
        net_locs[ref] = net_locs.get(ref, 0) + 1
      
    refs = []
    counts = [] 
    domains = []
    for domain in net_locs:
        counts.append(net_locs[domain])
        refs.append(domain)
        domains.append(dict(domain=domain,count=net_locs[domain]))
    values["domains"] = domains 
    values["refs"] = refs
    values["counts"] = counts    
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
        
def user(request,user_id = None, username =  None, timeframe = None):
    import datetime
    from django.utils import simplejson
    if not timeframe:
        time_delta = datetime.datetime.today() - datetime.timedelta(weeks=1)
    elif timeframe == "month":
        time_delta = datetime.datetime.today() - datetime.timedelta(weeks=4)
    elif timeframe == "year":
        time_delta = datetime.datetime.today() - datetime.timedelta(weeks=52)
    
    user = get_object_or_404(User, pk = user_id)
    
    values = default_values(request)
    
    values["links"] = user.link_set.all().order_by("-date_submitted").filter(date_submitted__gte=time_delta)
    v = [x.views for x in values["links"]]
    y = [x.clicks for x in values["links"]]
    values["totals"] = sum(v)
    values["totals2"] = sum(y)
    values["user"]  = user
    values["timeframe"]  = timeframe
    values["dateActivity"]  = Stat.objects.filter(link__user=user).filter(date__gte=time_delta).extra(select={"t":"DATE_FORMAT(`shortener_stat`.`date`, '%%d%%m%%Y')","date_is":"`shortener_stat`.`date`"}).values('t').annotate(activity=Count('stat_type'))
    
    if 'application/json' in request.META.get('HTTP_ACCEPT', '') or request.GET.get("format", None) == "json":
        new_values = {
            "links":values["links"].values('clicks','views', 'url','title')
        }

        data = simplejson.dumps(new_values)
        return HttpResponse(data,mimetype='application/json')
        
    return render_to_response(
        'shortener/user/main.html',
        values,
        context_instance=RequestContext(request))

def index(request):
    """
    View for main page (lists recent and popular links)
    """
    import datetime
    values = default_values(request)
    values['recent_links'] = Link.objects.all().order_by('-date_submitted')[0:10]    
    values['most_popular_links'] = Link.objects.filter(date_submitted__gte=(datetime.datetime.today() - datetime.timedelta(days=1)) ).annotate(num_clicks_views=Count('stat')).order_by('-num_clicks_views')[0:10]
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

