# Generated by Django 5.1.3 on 2024-12-06 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_alter_file_comment_alter_file_downloaded_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='size',
            field=models.IntegerField(),
        ),
    ]
