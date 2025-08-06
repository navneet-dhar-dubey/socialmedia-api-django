import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Post, Comment
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with users, posts, and comments.'

    def handle(self, *args, **options):
        # Initialize Faker
        fake = Faker()

        # Clear existing data
        self.stdout.write('Clearing old data...')
        User.objects.filter(is_superuser=False).delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()

        # --- Create Users ---
        self.stdout.write('Creating new users...')
        users = []
        for _ in range(5):
            username = fake.user_name()
            # Ensure username is unique
            while User.objects.filter(username=username).exists():
                username = fake.user_name() + str(random.randint(1, 100))
            
            user = User.objects.create_user(username=username, password='password123')
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(users)} users.'))

        # --- Create Posts ---
        self.stdout.write('Creating new posts...')
        posts = []
        for user in users:
            for _ in range(random.randint(2, 5)): # Each user creates 2 to 5 posts
                post = Post.objects.create(
                    author=user,
                    content=fake.paragraph(nb_sentences=5)
                )
                posts.append(post)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(posts)} posts.'))

        # --- Create Comments ---
        self.stdout.write('Creating new comments...')
        comments_count = 0
        for post in posts:
            for _ in range(random.randint(0, 7)): # Each post gets 0 to 7 comments
                Comment.objects.create(
                    author=random.choice(users), # Any user can comment
                    post=post,
                    content=fake.sentence()
                )
                comments_count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully created {comments_count} comments.'))

        self.stdout.write(self.style.SUCCESS('Database has been successfully seeded! 🌱'))