# Generated by Django 5.1.2 on 2024-11-02 06:22

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ombor', '0006_rename_maxsulot_nomi_korzinka_maxsulot_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='korzinka',
            name='user',
        ),
        migrations.RemoveField(
            model_name='olinganmaxsulotlar',
            name='user',
        ),
        migrations.CreateModel(
            name='Buyurtma',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='korzinka',
            name='buyurtma',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ombor.buyurtma'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='olinganmaxsulotlar',
            name='buyurtma',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ombor.buyurtma'),
            preserve_default=False,
        ),
    ]