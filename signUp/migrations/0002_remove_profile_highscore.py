# Generated by Django 2.2.14 on 2020-07-23 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signUp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='highScore',
        ),
    ]