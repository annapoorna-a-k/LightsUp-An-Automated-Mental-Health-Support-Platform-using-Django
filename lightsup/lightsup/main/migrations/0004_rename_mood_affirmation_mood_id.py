# Generated by Django 3.2.25 on 2024-12-11 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20241211_2331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='affirmation',
            old_name='mood',
            new_name='mood_id',
        ),
    ]
