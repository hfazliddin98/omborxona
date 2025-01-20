# Generated by Django 4.2.16 on 2025-01-19 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ombor', '0013_olinganmaxsulot_active_radetilganmaxsulot_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='olinganmaxsulot',
            name='maxsulot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ombor.maxsulot'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='olinganmaxsulot',
            name='qiymat',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='olinganmaxsulot',
            name='buyurtma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='olingan_maxsulotlar', to='ombor.buyurtma'),
        ),
    ]
