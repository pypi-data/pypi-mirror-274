# Generated by Django 5.0.2 on 2024-02-13 14:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("umap", "0016_pictogram_category"),
    ]

    operations = [
        migrations.RunSQL(
            "UPDATE social_auth_usersocialauth "
            "SET provider = 'openstreetmap-oauth2' WHERE provider = 'openstreetmap'"
        ),
    ]
