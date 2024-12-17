# Generated by Django 5.1.2 on 2024-11-01 09:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ombor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Birlik',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OmborniYopish',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('yopish', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='maxsulotnomi',
            name='kategoriya',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ombor.kategoriya'),
        ),
        migrations.CreateModel(
            name='Korzinka',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('qiymat', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=False)),
                ('tasdiqlash', models.BooleanField(default=False)),
                ('birlik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ombor.birlik')),
                ('kategoriya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ombor.kategoriya')),
                ('maxsulot_nomi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ombor.maxsulotnomi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ombor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('qiymat', models.CharField(max_length=255)),
                ('maxviylik', models.BooleanField(default=False)),
                ('birlik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ombor.birlik')),
                ('kategoriya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ombor.kategoriya')),
                ('maxsulot_nomi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ombor.maxsulotnomi')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
