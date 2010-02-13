from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Fetches the titles of webpages."

    args = ""

    def handle(self, **options):
        from urlweb.shortener.models import Link
        import httplib2 
        from BeautifulSoup import BeautifulSoup
        
        
        h = httplib2.Http(None)
        
        for link in Link.objects.filter(trys__gt=0):
            try:
                resp, content = h.request(link.url, "GET")
                if int(resp.status) == 200:
                    soup = BeautifulSoup(content)
                    titleTag = soup.html.head.title
                    link.title = titleTag.string
                    link.trys = 0
            except:
                pass
            link.trys = link.trys - 1
            link.save()
