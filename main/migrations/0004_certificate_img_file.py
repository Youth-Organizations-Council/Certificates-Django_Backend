# Generated by Django 4.1.2 on 2022-12-29 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_alter_organization_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="certificate",
            name="img_file",
            field=models.ImageField(blank=True, null=True, upload_to="certificates"),
        ),
    ]
