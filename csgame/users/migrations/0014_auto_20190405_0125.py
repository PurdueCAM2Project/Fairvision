# Generated by Django 2.1.7 on 2019-04-05 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_roundsnum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roundsnum',
            name='id',
        ),
        migrations.AddField(
            model_name='roundsnum',
            name='phase',
            field=models.CharField(default='phase01', max_length=10, primary_key=True, serialize=False),
        ),
    ]
