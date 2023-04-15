# Generated by Django 4.2 on 2023-04-15 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accueil', '0004_remove_client_image_client_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='save_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
