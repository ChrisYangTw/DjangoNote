# Generated by Django 4.0.3 on 2022-03-05 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_alter_teachers_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16, verbose_name='使用者帳號')),
                ('password', models.CharField(max_length=16, verbose_name='使用者密碼')),
                ('mobile', models.CharField(max_length=16, verbose_name='使用者電話')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
            ],
        ),
        migrations.AlterField(
            model_name='students',
            name='name',
            field=models.CharField(max_length=32, verbose_name='學生名稱'),
        ),
    ]