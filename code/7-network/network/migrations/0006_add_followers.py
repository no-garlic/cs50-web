# Generated by Django 5.2 on 2025-05-06 00:06

from django.db import migrations
import random


def add_data(apps, schema_editor):
    User = apps.get_model('network', 'User')
    Follow = apps.get_model('network', 'Follow')
    
    all_users = list(User.objects.all())
    
    for user in all_users:
        potential_followed_users = [other_user for other_user in all_users if other_user != user]
        num_to_follow = min(random.randint(3, 7), len(potential_followed_users))
        users_to_follow = random.sample(potential_followed_users, num_to_follow)
        for followed_user in users_to_follow:
            Follow.objects.create(follower=user, followed=followed_user)

def remove_data(apps, schema_editor):
    Follow = apps.get_model('network', 'Follow')
    Follow.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_add_likes'),
    ]

    operations = [
        migrations.RunPython(add_data, reverse_code=remove_data)
    ]
