# Generated by Django 2.2.16 on 2023-03-30 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20230330_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Выберете картинку для поста', upload_to='posts/', verbose_name='Картинка поста'),
        ),
    ]