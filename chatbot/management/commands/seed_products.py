# chatbot/management/commands/seed_products.py

from django.core.management.base import BaseCommand
from chatbot.models import Product
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Seed the database with mock product data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories = ['Electronics', 'Books', 'Textiles', 'Toys', 'Groceries']

        for _ in range(100):
            Product.objects.create(
                name=fake.unique.company(),
                description=fake.text(max_nb_chars=200),
                category=random.choice(categories),
                price=round(random.uniform(10.0, 1000.0), 2),
                stock=random.randint(5, 100),
                image_url=fake.image_url()
            )

        self.stdout.write(self.style.SUCCESS(
            "Successfully seeded 100 products"))
