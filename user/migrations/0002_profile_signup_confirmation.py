# Generated by Django 3.0.9 on 2020-08-20 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='signup_confirmation',
            field=models.BooleanField(default=False),
        ),
    ]
