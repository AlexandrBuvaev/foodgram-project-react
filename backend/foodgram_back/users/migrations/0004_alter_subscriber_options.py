# Generated by Django 3.2.16 on 2023-01-20 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230120_1043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriber',
            options={'verbose_name': 'Подпиcчик', 'verbose_name_plural': 'Подписчики'},
        ),
    ]
