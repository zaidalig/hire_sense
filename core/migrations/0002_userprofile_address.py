# Generated by Django 4.2 on 2025-07-14 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
