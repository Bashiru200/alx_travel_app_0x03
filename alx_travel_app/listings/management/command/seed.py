from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the databse with initial data'

    def handle(self, *args, **kwargs):
        host = User.objects.filter(is_staff=True).first()
        if not host:
            self.stderr.write("NO staff user found to host listings.")
            return