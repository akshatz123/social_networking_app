# Generated by Django 2.2.6 on 2019-11-01 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friendship', '0003_block_unique_together'),
        ('blog', '0009_user_friend_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='friend_name',
        ),
        migrations.AddField(
            model_name='user',
            name='friend_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='friendship.Friend'),
        ),
    ]
