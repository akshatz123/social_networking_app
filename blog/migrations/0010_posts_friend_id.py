# Generated by Django 2.2.7 on 2019-11-07 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friendship', '0003_block_unique_together'),
        ('blog', '0009_remove_posts_friend_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='friend_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='friendship.Friend'),
        ),
    ]
