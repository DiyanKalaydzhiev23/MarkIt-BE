# Generated by Django 5.0.2 on 2024-03-30 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze_file', '0003_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectPrompts',
        ),
    ]