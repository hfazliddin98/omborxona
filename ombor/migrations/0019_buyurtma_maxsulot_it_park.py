# Generated by Django 4.2.16 on 2024-12-05 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ombor', '0018_remove_talabnoma_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyurtma',
            name='maxsulot_it_park',
            field=models.BooleanField(default=False),
        ),
    ]