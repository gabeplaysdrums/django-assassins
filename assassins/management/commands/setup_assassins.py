from django.core.management.base import BaseCommand, CommandError
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Performs one-time setup tasks for the assassins app'

    def handle(self, *args, **options):
        self.stdout.write('Generating keys for encrypted fields')
        fieldkeys_dir = os.path.join(settings.BASE_DIR, 'fieldkeys')
        if os.path.exists(fieldkeys_dir):
            self.stdout.write('  ... Skipping ...')
        else:
            os.mkdir(fieldkeys_dir)
            os.system('keyczart create --location=%s --purpose=crypt' % (fieldkeys_dir,))
            os.system('keyczart addkey --location=%s --status=primary --size=256' % (fieldkeys_dir,))

        self.stdout.write('Success!')