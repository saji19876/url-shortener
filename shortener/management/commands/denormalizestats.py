from django.core.management.base import AppCommand

class Command(AppCommand):
    help = "Counts up the stats and updates the links."

    args = ""

    def handle_app(self, app, **options):
        from urlweb.shortener.models import Link
        
        for link in Link.objects.all():
            link.clicks = link.stat_set.filter(stat_type=1).count()
            link.views  = link.stat_set.filter(stat_type=2).count()
            link.save()
