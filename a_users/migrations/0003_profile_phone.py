# Generated by Django 5.0.6 on 2024-07-15 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0002_profile_gender_profile_interests'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]