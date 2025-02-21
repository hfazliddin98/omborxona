# Generated by Django 4.2.16 on 2025-01-20 06:22

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Buyurtma',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('maxsulot_role', models.CharField(choices=[('xojalik', 'xojalik'), ('rttm', 'rttm')], max_length=30)),
                ('buyurtma_role', models.CharField(choices=[('admin', 'admin'), ('prorektor', 'prorektor'), ('bugalter', 'bugalter'), ('xojalik', 'xojalik'), ('rttm', 'rttm'), ('omborchi', 'omborchi'), ('komendant', 'komendant')], max_length=30)),
                ('prorektor', models.BooleanField(default=False)),
                ('bugalter', models.BooleanField(default=False)),
                ('omborchi', models.BooleanField(default=False)),
                ('rttm', models.BooleanField(default=False)),
                ('xojalik', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('tasdiqlash', models.BooleanField(default=False)),
                ('rad_etish', models.BooleanField(default=False)),
                ('izoh', models.CharField(blank=True, max_length=355)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BuyurtmaMaxsulot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('qiymat', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JamiMahsulot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('qiymat', models.DecimalField(decimal_places=1, default=Decimal('0.00'), max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Kategoriya',
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
            name='Korzinka',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('maxsulot_role', models.CharField(choices=[('xojalik', 'xojalik'), ('rttm', 'rttm')], max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KorzinkaMaxsulot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('qiymat', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Maxsulot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('maxsulot_role', models.CharField(choices=[('xojalik', 'xojalik'), ('rttm', 'rttm')], default='xojalik', max_length=30)),
                ('maxviylik', models.BooleanField(default=False)),
                ('rasm', models.ImageField(null=True, upload_to='maxsulot')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OlinganMaxsulot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('qiymat', models.DecimalField(decimal_places=2, max_digits=10)),
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
                ('qiymat', models.DecimalField(decimal_places=2, max_digits=10)),
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
        migrations.CreateModel(
            name='Talabnoma',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('talabnoma_pdf', models.FileField(blank=True, null=True, upload_to='talabnoma_pdf')),
                ('active', models.BooleanField(default=True)),
                ('buyurtma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ombor.buyurtma')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RadEtilganMaxsulot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('buyurtma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ombor.buyurtma')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
