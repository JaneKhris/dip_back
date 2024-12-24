# Generated by Django 5.1.3 on 2024-12-24 10:25

from django.db import migrations
from django.conf import settings

def create_superuser(apps, editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    User.objects.create_superuser('chief_admin','email@email.com','password')


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser, migrations.RunPython.noop),
    ]