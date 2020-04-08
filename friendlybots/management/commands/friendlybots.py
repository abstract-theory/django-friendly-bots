from django.core.management.base import BaseCommand
from friendlybots.views import app_cache

class Command(BaseCommand):
    """
    Usage:
    ======
        Clear all items in this apps's cache.
        -------------------------------------
        django-admin friendlybots --clear
    """

    help = 'Django management commands for django-friendly-bots.'

    def add_arguments(self, parser):

        parser.add_argument(
            '--clear',
            action='store_true',
            help='Remove all items in the Friendly Bots cache.',
        )

    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))


    def handle(self, *args, **options):

        if options['clear']:
            self.success('    Friendly Bots cache deleted.')
            app_cache.clear()

        else:
            print('Add "--help" argument for command info.')
