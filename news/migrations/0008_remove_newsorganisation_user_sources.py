# Generated by Django 3.1.6 on 2021-02-17 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_newsorganisation_user_sources'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsorganisation',
            name='user_sources',
        ),
    ]
