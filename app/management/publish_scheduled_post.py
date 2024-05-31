# myapp/management/commands/publish_scheduled_posts.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import Post

class Command(BaseCommand):
    help = 'Publish scheduled posts'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        posts = Post.objects.filter(schedule_date__lte=now, is_published=False)
        for post in posts:
            post.is_published = True
            post.processed_date = now
            post.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully published post "{post.title}"'))
