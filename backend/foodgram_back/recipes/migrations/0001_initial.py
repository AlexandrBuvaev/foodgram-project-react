# Generated by Django 3.2.16 on 2023-01-19 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('color', models.CharField(max_length=16, verbose_name='Код цвет в НЕХ формате')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг тега')),
            ],
        ),
    ]