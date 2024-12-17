# Generated by Django 4.2.16 on 2024-11-27 14:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ombor', '0011_buyurtma_bugalter_buyurtma_it_park_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talabnoma',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('talabnoma_pdf', models.FileField(upload_to='talabnoma_pdf')),
                ('talabnoma_pdf_link', models.CharField(max_length=255)),
                ('buyurtma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ombor.buyurtma')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
