# Generated by Django 3.2.7 on 2022-09-13 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'user'), (2, 'staff'), (3, 'bot')], default=1),
        ),
    ]
