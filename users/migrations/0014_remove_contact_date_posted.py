# Generated by Django 2.2.10 on 2020-06-06 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='date_posted',
        ),
    ]
