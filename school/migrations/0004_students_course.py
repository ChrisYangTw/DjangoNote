# Generated by Django 4.0.3 on 2022-03-20 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_account_alter_students_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='course',
            field=models.ManyToManyField(to='school.courses'),
        ),
    ]
