# Generated by Django 5.0.2 on 2024-03-30 08:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_app', '0001_initial'),
        ('file_upload_router', '0002_delete_filerecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=255)),
                ('extension', models.CharField(max_length=10)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='auth_app.profile')),
            ],
        ),
    ]