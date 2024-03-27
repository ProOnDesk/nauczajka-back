import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Copy media files to another directory in docker container'

    def handle(self, *args, **options):
        # Get the absolute path of the source and destination directories
        source_dir = os.path.abspath(os.path.join(settings.BASE_DIR, 'media'))
        destination_dir = os.path.abspath(os.path.join(settings.MEDIA_ROOT, ))
        
        try:
            # Create the destination directory if it doesn't exist
            os.makedirs(destination_dir, exist_ok=True)

            # Copy the entire source directory with its contents to the destination directory
            shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)

            self.stdout.write(self.style.SUCCESS('Media files copied successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error copying media files: {str(e)}'))
