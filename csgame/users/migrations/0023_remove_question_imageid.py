# Generated by Django 2.1.7 on 2019-05-22 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20190521_0128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='imageID',
        ),
    ]
