# Generated by Django 4.2.16 on 2024-12-05 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ombor', '0017_alter_talabnoma_talabnoma_pdf_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talabnoma',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='talabnoma',
            name='talabnoma_pdf_link',
        ),
        migrations.RemoveField(
            model_name='talabnoma',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='talabnoma',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
