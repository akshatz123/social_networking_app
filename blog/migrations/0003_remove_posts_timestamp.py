# Generated by Django 2.2.6 on 2019-11-06 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_posts_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='timestamp',
        ),
    ]
