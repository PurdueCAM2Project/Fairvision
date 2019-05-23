# Generated by Django 2.1.7 on 2019-02-22 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190222_0710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zipfile',
            name='taboo1',
        ),
        migrations.RemoveField(
            model_name='zipfile',
            name='taboo2',
        ),
        migrations.RemoveField(
            model_name='zipfile',
            name='taboo3',
        ),
        migrations.RemoveField(
            model_name='zipfile',
            name='tb1',
        ),
        migrations.RemoveField(
            model_name='zipfile',
            name='tb2',
        ),
        migrations.RemoveField(
            model_name='zipfile',
            name='tb3',
        ),
        migrations.AddField(
            model_name='zipfile',
            name='taboo_words_1',
            field=models.CharField(default='N/A', max_length=20, verbose_name='Taboo Word 1'),
        ),
        migrations.AddField(
            model_name='zipfile',
            name='taboo_words_2',
            field=models.CharField(default='N/A', max_length=20, verbose_name='Taboo Word 2'),
        ),
        migrations.AddField(
            model_name='zipfile',
            name='taboo_words_3',
            field=models.CharField(default='N/A', max_length=20, verbose_name='Taboo Word 3'),
        ),
        migrations.AddField(
            model_name='zipfile',
            name='tb',
            field=models.ManyToManyField(related_name='taboowords', to='users.Label'),
        ),
    ]