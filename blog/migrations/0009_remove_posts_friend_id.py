# Generated by Django 2.2.7 on 2019-11-07 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20191107_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='friend_id',
        ),
    ]
