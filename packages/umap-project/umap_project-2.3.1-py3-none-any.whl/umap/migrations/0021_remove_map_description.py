# Generated by Django 5.0.4 on 2024-04-24 07:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("umap", "0020_alter_tilelayer_url_template"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="map",
            name="description",
        ),
    ]
