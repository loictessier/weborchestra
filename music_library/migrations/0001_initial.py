# Generated by Django 3.0.9 on 2020-12-10 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MusicScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50, unique=True, verbose_name='Nom')),
                ('author', models.TextField(max_length=50, verbose_name='Auteur')),
                ('editor', models.TextField(max_length=50, verbose_name='Editeur')),
            ],
        ),
    ]
