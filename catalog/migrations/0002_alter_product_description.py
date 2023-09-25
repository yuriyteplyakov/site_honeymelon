# Generated by Django 4.2.4 on 2023-09-19 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(
                blank=True, help_text="не более 200 символов", max_length=200, null=True
            ),
        ),
    ]
