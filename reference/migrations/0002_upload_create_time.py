# Generated by Django 4.0.2 on 2022-02-28 16:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='δΈε³ζι'),
            preserve_default=False,
        ),
    ]
